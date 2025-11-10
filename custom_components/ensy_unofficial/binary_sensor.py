from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.ensy_unofficial.client import EnsyClient, EnsyState
from custom_components.ensy_unofficial.const import DOMAIN, get_device_info


class EnsyBinarySensor(BinarySensorEntity):
    _attr_should_poll = False

    def __init__(
        self, ensy_client: EnsyClient, name: str, state_key: str, device_name: str
    ) -> None:
        self._ensy_client = ensy_client
        self._attr_name = name
        self._state_key = state_key
        self._attr_unique_id = (
            f"binary_sensor_{DOMAIN}_{ensy_client.mac_address}_{state_key}"
        )
        self._attr_is_on: bool | None = None
        self._attr_device_info = get_device_info(ensy_client.mac_address, device_name)

    async def async_added_to_hass(self) -> None:
        self._ensy_client.on_state_updated.append(self._on_state_change)  # type: ignore

    def _on_state_change(self, state: EnsyState) -> None:
        # value is the raw MQTT value, we get the type coerced one out of state:
        value = getattr(state, self._state_key)
        if value == self._attr_is_on:
            return
        assert isinstance(value, bool)

        self._attr_is_on = value
        self.schedule_update_ha_state()


class EnsyHeaterSensor(EnsyBinarySensor):
    _attr_device_class = BinarySensorDeviceClass.HEAT


class EnsyOnlineSensor(EnsyBinarySensor):
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    ensy_client = hass.data[DOMAIN][entry.entry_id]
    device_name = entry.data.get("name", "Ensy Ventilation Aggregate")
    
    sensors = [
        EnsyHeaterSensor(ensy_client, "Heater element", "is_heating", device_name),
        EnsyOnlineSensor(ensy_client, "Connectivity", "is_online", device_name),
    ]
    async_add_entities(sensors)
