"""The ZCS Azzurro integration."""
from __future__ import annotations
import logging

from datetime import timedelta
import flatdict

from homeassistant.components import persistent_notification
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_CLIENT_ID, CONF_CLIENT_SECRET, CONF_NAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
import voluptuous as vol

from .api import ZCSPortal
from .const import (
    API,
    API_POLL_INTERVAL,
    COORDINATOR,
    CONF_AUTH_KEY,
    CONF_CLIENT_CODE,
    CONF_THING_KEY,
    DOMAIN,
    MANUFACTURER,
)

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA_ROOT = vol.Schema(
    {
        vol.Required(CONF_AUTH_KEY): cv.string,
        vol.Required(CONF_CLIENT_CODE): cv.string,
    }
)

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: CONFIG_SCHEMA_ROOT},
    extra=vol.ALLOW_EXTRA,
)

PLATFORMS = [
    Platform.SENSOR,
]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the ZCS Azzurro component."""
    hass.data[DOMAIN] = {}

    if DOMAIN not in config:
        persistent_notification.async_create(
            hass,
            "In order to setup ZCS Azzurro component, add to configuration.yaml "
            "the configuration with yout client code and auth key. Then you can "
            "add devices through integrations interface. See documentation.",
            MANUFACTURER,
            "zcsazzurro_config",
        )
        return False

    hass.data[DOMAIN][CONF_AUTH_KEY] = config[DOMAIN][CONF_AUTH_KEY]
    hass.data[DOMAIN][CONF_CLIENT_CODE] = config[DOMAIN][CONF_CLIENT_CODE]

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ZCS Azzurro from a config entry."""

    hass.data[DOMAIN][entry.entry_id] = {}
    hass.data[DOMAIN][entry.entry_id][CONF_THING_KEY] = entry.data[CONF_THING_KEY]
    hass.data[DOMAIN][entry.entry_id][API] = ZCSPortal(
        hass,
        hass.data[DOMAIN][CONF_CLIENT_CODE],
        hass.data[DOMAIN][CONF_AUTH_KEY],
        entry.data[CONF_THING_KEY],
    )

    coordinator = await get_coordinator(hass, entry)
    if not coordinator.last_update_success:
        await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def get_coordinator(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> DataUpdateCoordinator:
    """Get the data update coordinator."""
    if COORDINATOR in hass.data[DOMAIN][entry.entry_id]:
        return hass.data[DOMAIN][entry.entry_id][COORDINATOR]

    async def async_fetch():
        zcs_portal = hass.data[DOMAIN][entry.entry_id][API]

        result = await zcs_portal.fetch_real_time_data()

        flat_result: dict = {}
        try:
            for ent in result:
                flat_result[ent] = dict(
                    flatdict.FlatterDict(result[ent], delimiter="|")
                )
        except TypeError as ex:
            raise UpdateFailed(ex) from ex

        _LOGGER.debug("Data: %s", flat_result)
        return flat_result

    hass.data[DOMAIN][entry.entry_id][COORDINATOR] = DataUpdateCoordinator(
        hass,
        logging.getLogger(__name__),
        name=DOMAIN,
        update_method=async_fetch,
        update_interval=timedelta(seconds=API_POLL_INTERVAL),
    )
    await hass.data[DOMAIN][entry.entry_id][COORDINATOR].async_refresh()
    return hass.data[DOMAIN][entry.entry_id][COORDINATOR]
