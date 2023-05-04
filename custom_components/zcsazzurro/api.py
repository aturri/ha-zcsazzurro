"""API for ZCS Azzurro bound to Home Assistant OAuth."""
import json
import logging

from homeassistant.components.rest.const import DEFAULT_SSL_CIPHER_LIST
from homeassistant.components.rest.data import RestData
from homeassistant.core import HomeAssistant

from .const import API_READ_TIMEOUT

ZCS_ENDPOINT = "https://third.zcsazzurroportal.com:19003"

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

        if api_result is not None:
            try:
                thing_result = api_result["realtimeData"]["params"]["value"][0][
                    self._thing_key
                ]
            except KeyError:
                _LOGGER.warning("Unable to read result from ZCS Azzurro portal")

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

        if rest.data is None:
            _LOGGER.warning("Unable to fetch data from ZCS Azzurro portal")
            return None

        try:
            return json.loads(rest.data)
        except json.decoder.JSONDecodeError:
            _LOGGER.warning("Unable to parse result from ZCS Azzurro portal")

        return None
