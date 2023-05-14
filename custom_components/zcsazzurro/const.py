"""Constants for the ZCS Azzurro integration."""

DOMAIN = "zcsazzurro"
VERSION = "0.0.7"
API_READ_TIMEOUT = 30
API_POLL_INTERVAL = 300
MANUFACTURER = "ZCS Azzurro"

# Conf keys
CONF_THING_KEY = "thing_key"
CONF_AUTH_KEY = "auth_key"
CONF_CLIENT_CODE = "client_code"

API = "api"
COORDINATOR = "coordinator"

STATUS_ICON = {
    "generating_consuming_from_network": "mdi:solar-power-variant-outline",
    "generating_consuming_from_produced": "mdi:solar-power-variant-outline",
    "generating": "mdi:solar-power-variant-outline",
    "consuming_from_network": "mdi:transmission-tower-export",
    "consuming_from_produced": "mdi:home-battery-outline",
}
