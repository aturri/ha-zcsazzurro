"""API for ZCS Azzurro bound to Home Assistant OAuth."""
from datetime import timedelta
import json
import logging

import httpx

from homeassistant.components.rest.const import DEFAULT_SSL_CIPHER_LIST
from homeassistant.components.rest.data import RestData
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

from .const import API_READ_TIMEOUT

ZCS_ENDPOINT = "https://third.zcsazzurroportal.com:19003"
ZCS_502_ERROR = "502 Proxy Error"
ZCS_503_ERROR = "503 Service Unavailable"

_LOGGER = logging.getLogger(__name__)


class ZCSPortal:
    """Provide class to wrap ZCS Azzurro portal API."""

    def __init__(
        self,
        hass: HomeAssistant,
        client_code: str,
        auth_key: str,
        thing_key: str,
    ) -> None:
        """Create object representing ZCS API."""
        self._hass = hass
        self._client_code = client_code
        self._auth_key = auth_key
        self._thing_key = thing_key
        self._auth_key = auth_key

    async def fetch_real_time_data(self):
        """Fetch real time data from ZCS Azzurro portal."""
        now = dt_util.utcnow()
        start = (now - timedelta(hours=8)).strftime("%Y-%m-%dT%H:%M:%SZ")
        end = now.strftime("%Y-%m-%dT%H:%M:%SZ")

        _LOGGER.debug(
            "Requesting real-time and historic (%s -> %s) data for %s",
            start,
            end,
            self._thing_key,
        )

        payload = {
            "historicData": {
                "command": "historicData",
                "params": {
                    "start": start,
                    "end": end,
                    "thingKey": self._thing_key,
                    "requiredValues": "ts,currentDC,voltageDC,powerDC,temperature,energyGeneratingTotal,energyGenerating,powerGenerating",
                },
            },
            "realtimeData": {
                "command": "realtimeData",
                "params": {
                    "thingKey": self._thing_key,
                    "requiredValues": "*",
                },
            },
        }

        api_result = await self._fetch_data(payload)
        thing_result = {}
        use_cached_result = False

        if api_result[1] is not None:
            real_time_data = await self._read_real_time_data(api_result[1])
            historic_data = await self._read_historic_data(
                api_result[1], real_time_data.get("lastUpdate")
            )
            thing_result = real_time_data | historic_data
            if thing_result.get("lastUpdate") is None:
                thing_result = {}
                use_cached_result = True

        elif api_result[0] not in range(400, 500):
            use_cached_result = True

        thing_result["_use_cached_result"] = use_cached_result
        result = {}
        result[self._thing_key] = thing_result
        return result

    async def _fetch_data(self, payload: dict, timeout: int = API_READ_TIMEOUT):
        """Fetch data from ZCS Azzurro portal."""

        string_payload = json.dumps(payload)

        headers = {
            "Client": self._client_code,
            "Authorization": self._auth_key,
        }

        rest = RestData(
            self._hass,
            "POST",
            ZCS_ENDPOINT,
            "utf8",
            None,
            headers,
            None,
            string_payload,
            False,
            DEFAULT_SSL_CIPHER_LIST,
            timeout,
        )
        await rest.async_update()

        if rest.data is None and isinstance(
            rest.last_exception, httpx.TimeoutException
        ):
            _LOGGER.warning(
                "Timeout fetching data from ZCS Azzurro portal at %s", ZCS_ENDPOINT
            )
            return (0, None)

        if rest.data is None:
            message = (
                "unknown reason"
                if rest.last_exception is None
                else str(rest.last_exception)
            )
            _LOGGER.error(
                "Error fetching data from ZCS Azzurro portal, reason is: %s", message
            )
            return (400, None)

        if ZCS_502_ERROR in rest.data:
            _LOGGER.warning("ZCS Azzurro portal is unavailable: %s", ZCS_502_ERROR)
            return (502, None)

        if ZCS_503_ERROR in rest.data:
            _LOGGER.warning("ZCS Azzurro portal is unavailable: %s", ZCS_503_ERROR)
            return (503, None)

        try:
            return (200, json.loads(rest.data))
        except json.decoder.JSONDecodeError:
            _LOGGER.warning(
                "Unable to parse result from ZCS Azzurro portal: %s", rest.data
            )
            return (500, None)

    async def _read_real_time_data(self, api_result):
        real_time_data = {}
        try:
            real_time_data = api_result["realtimeData"]["params"]["value"][0][
                self._thing_key
            ]
        except KeyError:
            _LOGGER.warning(
                "No real-time data in response from ZCS Azzurro portal for %s",
                self._thing_key,
            )
        return real_time_data

    async def _read_historic_data(self, api_result, real_time_ts):
        historic_data = {}
        try:
            historic_data_raw = api_result["historicData"]["params"]["value"][0][
                self._thing_key
            ]
            historic_data_idx = len(historic_data_raw["ts"]) - 1
            if historic_data_idx < 0:
                return historic_data
            historic_ts = historic_data_raw["ts"][historic_data_idx]
            if real_time_ts is None or (
                historic_ts is not None
                and dt_util.parse_datetime(historic_ts)
                > dt_util.parse_datetime(real_time_ts)
            ):
                historic_data["lastUpdate"] = historic_ts
                historic_data["powerGenerating"] = historic_data_raw["powerGenerating"][
                    historic_data_idx
                ]
                historic_data["energyGenerating"] = historic_data_raw[
                    "energyGenerating"
                ][historic_data_idx]
                historic_data["energyGeneratingTotal"] = historic_data_raw[
                    "energyGeneratingTotal"
                ][historic_data_idx]
            historic_data["currentDC"] = historic_data_raw["currentDC"][
                historic_data_idx
            ]
            historic_data["voltageDC"] = historic_data_raw["voltageDC"][
                historic_data_idx
            ]
            historic_data["powerDC"] = historic_data_raw["powerDC"][historic_data_idx]
            historic_data["temperature"] = historic_data_raw["temperature"][
                historic_data_idx
            ]
        except KeyError:
            _LOGGER.warning(
                "No historic data in response from ZCS Azzurro portal for %s",
                self._thing_key,
            )
        return historic_data
