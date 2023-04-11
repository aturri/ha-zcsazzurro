"""Config flow for ZCS Azzurro."""
from __future__ import annotations

from homeassistant.config_entries import CONN_CLASS_CLOUD_POLL, ConfigFlow
import voluptuous as vol

from .const import CONF_THING_KEY, DOMAIN


class ZCSAzzurroConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow to handle ZCS Azzurro entry"""

    VERSION = 1
    CONNECTION_CLASS = CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize config flow."""
        self._thing_key = None

    async def _show_setup_form(self, errors=None):
        """Show the setup form to the user."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_THING_KEY): str,
                },
            ),
            errors=errors or {},
            last_step=True,
        )

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        if user_input is None:
            return await self._show_setup_form(user_input)

        self._thing_key = user_input[CONF_THING_KEY]

        await self.async_set_unique_id(f"{self._thing_key}")
        self._abort_if_unique_id_configured()

        return self._async_create_entry()

    def _async_create_entry(self):
        """Handle create entry."""
        return self.async_create_entry(
            title=f"{self._thing_key}",
            data={
                CONF_THING_KEY: self._thing_key,
            },
        )
