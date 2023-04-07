"""Diagnostics support for ZCS Azzurro."""
from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import CONF_THING_KEY, COORDINATOR, DOMAIN

TO_REDACT = {CONF_THING_KEY, "serial"}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> dict:
    """Return diagnostics for a config entry."""
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        COORDINATOR
    ]

    thing_key = config_entry.data[CONF_THING_KEY]
    device_data = coordinator.data[thing_key]

    diagnostics_data = {
        "info": async_redact_data(config_entry.data, TO_REDACT),
        "data": async_redact_data(device_data, TO_REDACT),
    }

    return diagnostics_data


async def async_get_device_diagnostics(
    hass: HomeAssistant, config_entry: ConfigEntry, device: DeviceEntry
) -> dict[str, Any]:
    """Return diagnostics for a device."""
    info = {}
    info["manufacturer"] = device.manufacturer
    info["serial"] = config_entry.data[CONF_THING_KEY]

    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        COORDINATOR
    ]

    device_data = {}

    for key in coordinator.data:
        device_data = coordinator.data[key]

    diagnostics_data = {
        "info": async_redact_data(info, TO_REDACT),
        "data": async_redact_data(device_data, TO_REDACT),
    }

    return diagnostics_data
