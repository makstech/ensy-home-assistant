"""Constants for the ensy (unofficial) integration."""

from homeassistant.components.mqtt.const import CONF_TLS_INSECURE
from homeassistant.const import CONF_MAC, CONF_NAME
from homeassistant.helpers.device_registry import DeviceInfo

DOMAIN = "ensy_unofficial"
DEFAULT_NAME = "Ensy Ventilation Aggregate"
DEFAULT_CONF_TLS_INSECURE = False


def get_device_info(mac_address: str, name: str) -> DeviceInfo:
    """Get the shared device info for all entities."""
    return DeviceInfo(
        identifiers={(DOMAIN, mac_address)},
        name=name,
        manufacturer="Ensy",
        model="InoVent",
    )


__all__ = [
    "CONF_MAC",
    "CONF_NAME",
    "CONF_TLS_INSECURE",
    "DEFAULT_NAME",
    "DOMAIN",
    "get_device_info",
]
