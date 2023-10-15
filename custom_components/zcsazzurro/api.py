"""API for ZCS Azzurro bound to Home Assistant OAuth."""
import json
import logging

import httpx

from homeassistant.components.rest.const import DEFAULT_SSL_CIPHER_LIST
from homeassistant.components.rest.data import RestData
from homeassistant.core import HomeAssistant

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

        payload = {
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
            try:
                thing_result = api_result[1]["realtimeData"]["params"]["value"][0][
                    self._thing_key
                ]
            except KeyError:
                _LOGGER.warning(
                    "No data in response from ZCS Azzurro portal for %s",
                    self._thing_key,
                )
        elif api_result[0] in range(500, 600):
            use_cached_result = True

        result = {}
        result[self._thing_key] = thing_result
        result["_use_cached_result"] = use_cached_result
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
