"""Platform for ZCS Azzurro sensor integration."""
from __future__ import annotations
import logging

from dataclasses import dataclass
from typing import Any, Final

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import UnitOfEnergy, UnitOfPower, PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.util import dt

from . import get_coordinator
from .const import (
    DOMAIN,
    MANUFACTURER,
)

_LOGGER = logging.getLogger(__name__)


@dataclass
class ZCSSensorDescription(SensorEntityDescription):
    """Class describing ZCS Azzurro sensor entities."""

    data_tag: str | None = None
    extra_attributes: dict[str, Any] | None = None


@dataclass
class ZCSSensorDefinition:
    """Class for defining sensor entities."""

    description: ZCSSensorDescription = None


SENSOR_TYPES: Final[tuple[ZCSSensorDefinition, ...]] = (
    ZCSSensorDefinition(
        description=ZCSSensorDescription(
            key="status",
            translation_key="status",
            icon="mdi:solar-panel-large",
            extra_attributes={
                "last_update": None,
                "first_update": None,
            },
        ),
    ),
    ZCSSensorDefinition(
        description=ZCSSensorDescription(
            key="power_generating",
            data_tag="powerGenerating",
            device_class=SensorDeviceClass.POWER,
            translation_key="power_generating",
            native_unit_of_measurement=UnitOfPower.WATT,
            state_class=SensorStateClass.MEASUREMENT,
            icon="mdi:solar-power-variant",
        ),
    ),
    ZCSSensorDefinition(
        description=ZCSSensorDescription(
            key="energy_generating_today",
            data_tag="energyGenerating",
            device_class=SensorDeviceClass.ENERGY,
            translation_key="energy_generating_today",
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            state_class=SensorStateClass.TOTAL_INCREASING,
            icon="mdi:solar-power",
        ),
    ),
    ZCSSensorDefinition(
        description=ZCSSensorDescription(
            key="energy_generating_total",
            data_tag="energyGeneratingTotal",
            device_class=SensorDeviceClass.ENERGY,
            translation_key="energy_generating_total",
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            state_class=SensorStateClass.TOTAL,
            icon="mdi:solar-power",
        ),
    ),
    ZCSSensorDefinition(
        description=ZCSSensorDescription(
            key="power_consuming",
            data_tag="powerConsuming",
            device_class=SensorDeviceClass.POWER,
            translation_key="power_consuming",
            native_unit_of_measurement=UnitOfPower.WATT,
            state_class=SensorStateClass.MEASUREMENT,
            icon="mdi:power-plug",
            entity_registry_enabled_default=False,
        ),
    ),
    ZCSSensorDefinition(
        description=ZCSSensorDescription(
            key="energy_consuming_today",
            data_tag="energyConsuming",
            device_class=SensorDeviceClass.ENERGY,
            translation_key="energy_consuming_today",
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            state_class=SensorStateClass.TOTAL_INCREASING,
            icon="mdi:power-plug-outline",
            entity_registry_enabled_default=False,
        ),
    ),
    ZCSSensorDefinition(
        description=ZCSSensorDescription(
            key="energy_consuming_total",
            data_tag="energyConsumingTotal",
            device_class=SensorDeviceClass.ENERGY,
            translation_key="energy_consuming_total",
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            state_class=SensorStateClass.TOTAL,
            icon="mdi:power-plug-outline",
            entity_registry_enabled_default=False,
        ),
    ),
    ZCSSensorDefinition(
        description=ZCSSensorDescription(
            key="power_autoconsuming",
            data_tag="powerAutoconsuming",
            device_class=SensorDeviceClass.POWER,
            translation_key="power_autoconsuming",
            native_unit_of_measurement=UnitOfPower.WATT,
            state_class=SensorStateClass.MEASUREMENT,
            icon="mdi:home-lightning-bolt",
            entity_registry_enabled_default=False,
        ),
    ),
    ZCSSensorDefinition(
        description=ZCSSensorDescription(
            key="energy_autoconsuming_today",
            data_tag="energyAutoconsuming",
            device_class=SensorDeviceClass.ENERGY,
            translation_key="energy_autoconsuming_today",
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            state_class=SensorStateClass.TOTAL_INCREASING,
            icon="mdi:home-lightning-bolt-outline",
            entity_registry_enabled_default=False,
        ),
    ),
    ZCSSensorDefinition(
        description=ZCSSensorDescription(
            key="energy_autoconsuming_total",
            data_tag="energyAutoconsumingTotal",
            device_class=SensorDeviceClass.ENERGY,
            translation_key="energy_autoconsuming_total",
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            state_class=SensorStateClass.TOTAL,
            icon="mdi:home-lightning-bolt-outline",
            entity_registry_enabled_default=False,
        ),
    ),
    ZCSSensorDefinition(
        description=ZCSSensorDescription(
            key="power_charging",
            data_tag="powerCharging",
            device_class=SensorDeviceClass.POWER,
            translation_key="power_charging",
            native_unit_of_measurement=UnitOfPower.WATT,
            state_class=SensorStateClass.MEASUREMENT,
            icon="mdi:battery-charging",
            entity_registry_enabled_default=False,
        ),
    ),
    ZCSSensorDefinition(
        description=ZCSSensorDescription(
            key="energy_charging_today",
            data_tag="energyCharging",
            device_class=SensorDeviceClass.ENERGY,
            translation_key="energy_charging_today",
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            state_class=SensorStateClass.TOTAL_INCREASING,
            icon="mdi:battery-charging-outline",
            entity_registry_enabled_default=False,
        ),
    ),
    ZCSSensorDefinition(
        description=ZCSSensorDescription(
            key="energy_charging_total",
            data_tag="energyChargingTotal",
            device_class=SensorDeviceClass.ENERGY,
            translation_key="energy_charging_total",
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            state_class=SensorStateClass.TOTAL,
            icon="mdi:battery-charging-outline",
            entity_registry_enabled_default=False,
        ),
    ),
    ZCSSensorDefinition(
        description=ZCSSensorDescription(
            key="power_discharging",
            data_tag="powerDischarging",
            device_class=SensorDeviceClass.POWER,
            translation_key="power_discharging",
            native_unit_of_measurement=UnitOfPower.WATT,
            state_class=SensorStateClass.MEASUREMENT,
            icon="mdi:power-plug-battery",
            entity_registry_enabled_default=False,
        ),
    ),
    ZCSSensorDefinition(
        description=ZCSSensorDescription(
            key="energy_discharging_today",
            data_tag="energyDischarging",
            device_class=SensorDeviceClass.ENERGY,
            translation_key="energy_discharging_today",
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            state_class=SensorStateClass.TOTAL_INCREASING,
            icon="mdi:power-plug-battery-outline",
            entity_registry_enabled_default=False,
        ),
    ),
    ZCSSensorDefinition(
        description=ZCSSensorDescription(
            key="energy_discharging_total",
            data_tag="energyDischargingTotal",
            device_class=SensorDeviceClass.ENERGY,
            translation_key="energy_discharging_total",
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            state_class=SensorStateClass.TOTAL,
            icon="mdi:power-plug-battery-outline",
            entity_registry_enabled_default=False,
        ),
    ),
    ZCSSensorDefinition(
        description=ZCSSensorDescription(
            key="power_importing",
            data_tag="powerImporting",
            device_class=SensorDeviceClass.POWER,
            translation_key="power_importing",
            native_unit_of_measurement=UnitOfPower.WATT,
            state_class=SensorStateClass.MEASUREMENT,
            icon="mdi:transmission-tower-import",
            entity_registry_enabled_default=False,
        ),
    ),
    ZCSSensorDefinition(
        description=ZCSSensorDescription(
            key="energy_importing_today",
            data_tag="energyImporting",
            device_class=SensorDeviceClass.ENERGY,
            translation_key="energy_importing_today",
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            state_class=SensorStateClass.TOTAL_INCREASING,
            icon="mdi:transmission-tower-import",
            entity_registry_enabled_default=False,
        ),
    ),
    ZCSSensorDefinition(
        description=ZCSSensorDescription(
            key="energy_importing_total",
            data_tag="energyImportingTotal",
            device_class=SensorDeviceClass.ENERGY,
            translation_key="energy_importing_total",
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            state_class=SensorStateClass.TOTAL,
            icon="mdi:transmission-tower-import",
            entity_registry_enabled_default=False,
        ),
    ),
    ZCSSensorDefinition(
        description=ZCSSensorDescription(
            key="power_exporting",
            data_tag="powerExporting",
            device_class=SensorDeviceClass.POWER,
            translation_key="power_exporting",
            native_unit_of_measurement=UnitOfPower.WATT,
            state_class=SensorStateClass.MEASUREMENT,
            icon="mdi:transmission-tower-export",
            entity_registry_enabled_default=False,
        ),
    ),
    ZCSSensorDefinition(
        description=ZCSSensorDescription(
            key="energy_exporting_today",
            data_tag="energyExporting",
            device_class=SensorDeviceClass.ENERGY,
            translation_key="energy_exporting_today",
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            state_class=SensorStateClass.TOTAL_INCREASING,
            icon="mdi:transmission-tower-export",
            entity_registry_enabled_default=False,
        ),
    ),
    ZCSSensorDefinition(
        description=ZCSSensorDescription(
            key="energy_exporting_total",
            data_tag="energyExportingTotal",
            device_class=SensorDeviceClass.ENERGY,
            translation_key="energy_exporting_total",
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            state_class=SensorStateClass.TOTAL,
            icon="mdi:transmission-tower-export",
            entity_registry_enabled_default=False,
        ),
    ),
    ZCSSensorDefinition(
        description=ZCSSensorDescription(
            key="battery_soc",
            data_tag="batterySoC",
            device_class=SensorDeviceClass.BATTERY,
            translation_key="battery_soc",
            native_unit_of_measurement=PERCENTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            entity_registry_enabled_default=False,
        ),
    ),
    ZCSSensorDefinition(
        description=ZCSSensorDescription(
            key="battery_soc_2",
            data_tag="batterySoC2",
            device_class=SensorDeviceClass.BATTERY,
            translation_key="battery_soc_2",
            native_unit_of_measurement=PERCENTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            entity_registry_enabled_default=False,
        ),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigType,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = await get_coordinator(hass, config_entry)

    entities = []
    for idx, thing_key in enumerate(coordinator.data):
        for definition in SENSOR_TYPES:
            entities.append(
                ZCSSensor(coordinator, idx, thing_key, definition.description)
            )

    async_add_entities(entities)


class ZCSSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""

    entity_description: ZCSSensorDescription

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        idx,
        thing_key,
        description: ZCSSensorDescription,
    ):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._idx = idx
        self._thing_key = thing_key
        self.entity_description = description
        self._attr_has_entity_name = True
        self._attr_unique_id = f"{self.entity_description.key}-{self._thing_key}"
        _LOGGER.debug("init sensor %s", self._attr_unique_id)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._thing_key)},
            name=self._thing_key,
            manufacturer=MANUFACTURER,
        )

    @property
    def native_value(self):
        """Return the state of the sensor."""
        # status sensors have a special function based on observed values
        if (
            self.entity_description.data_tag is None
            and self.entity_description.key == "status"
        ):
            return self._read_status()

        # return None when there is not the required key
        if (
            self.coordinator.data[self._thing_key].get(self.entity_description.data_tag)
            is None
        ):
            return None

        # on total increasing sensors, force value to 0 at start of local day until first value is shown
        # by ZCS device to avoid messing up energy stats
        if (
            self.entity_description.device_class == SensorDeviceClass.ENERGY
            and self.entity_description.state_class == SensorStateClass.TOTAL_INCREASING
            and self._read_last_update() is not None
        ):
            last_update = dt.parse_datetime(self._read_last_update())
            start_of_day = dt.start_of_local_day()
            if last_update is not None and start_of_day > last_update:
                _LOGGER.debug(
                    "Last seen ZCS device at %s, start of day is at %s, forcing energy measurement to 0 to reset cycle",
                    last_update,
                    start_of_day,
                )
                return 0

        # by default, return raw value from the coordinator data
        return self.coordinator.data[self._thing_key].get(
            self.entity_description.data_tag
        )

    @property
    def available(self):
        """Return the availability of the entity."""

        if not self.coordinator.last_update_success:
            return False

        return True

    @property
    def extra_state_attributes(self):
        attr = {}
        if self.entity_description.extra_attributes is not None:
            attr = self.entity_description.extra_attributes

            if "last_update" in self.entity_description.extra_attributes:
                attr["last_update"] = self._read_last_update()

            if "first_update" in self.entity_description.extra_attributes:
                attr["first_update"] = self._read_first_update()

        attr["serial"] = self._thing_key

        return attr

    def _read_status(self):
        power_generating = self.coordinator.data[self._thing_key].get("powerGenerating")
        power_consuming = self.coordinator.data[self._thing_key].get("powerConsuming")
        power_autoconsuming = self.coordinator.data[self._thing_key].get(
            "powerAutoconsuming"
        )

        is_generating = power_generating is not None and power_generating > 0
        is_consuming = power_consuming is not None and power_consuming > 0
        is_autoconsuming = power_autoconsuming is not None and power_autoconsuming > 0

        if is_generating and is_consuming:
            return "generating_consuming_from_network"

        if is_generating and is_autoconsuming:
            return "generating_consuming_from_produced"

        if is_generating:
            return "generating"

        if is_consuming:
            return "consuming_from_network"

        if is_autoconsuming:
            return "consuming_from_produced"

        return "idle"

    def _read_last_update(self):
        return self.coordinator.data[self._thing_key].get("lastUpdate")

    def _read_first_update(self):
        return self.coordinator.data[self._thing_key].get("thingFind")
