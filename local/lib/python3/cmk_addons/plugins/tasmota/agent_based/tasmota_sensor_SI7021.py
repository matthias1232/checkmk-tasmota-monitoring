#!/usr/bin/env python3

# Beispiel-Agent-Output (nur Dokumentation, wird NICHT geparst):
# <<<check_mk>>>
# Version: Tasmota Special Agent 1.0
# AgentOS: linux
# <<<tasmota_status:sep(0)>>>
# {"StatusSNS":{"Time":"2025-11-23T16:33:31","SI7021":{"Temperature":30.5,"Humidity":58.6,"DewPoint":21.5},"TempUnit":"C"}}

from collections.abc import Mapping
from typing import Any

from cmk.agent_based.v2 import (
    CheckPlugin,
    get_value_store,
    CheckResult,
    DiscoveryResult,
    Service,
    Result,
    State,
)
from cmk.plugins.lib.temperature import check_temperature, TempParamType
from cmk.plugins.lib.humidity import check_humidity

# -------- Discovery: SI7021 --------


def discover_tasmota_si7021_temperature(section: Mapping[str, Any]) -> DiscoveryResult:
    si7021 = section.get("StatusSNS", {}).get("SI7021", {})
    if isinstance(si7021, dict) and "Temperature" in si7021:
        yield Service(item="Temperature")


def discover_tasmota_si7021_dewpoint(section: Mapping[str, Any]) -> DiscoveryResult:
    si7021 = section.get("StatusSNS", {}).get("SI7021", {})
    if isinstance(si7021, dict) and "DewPoint" in si7021:
        yield Service(item="DewPoint")


def discover_tasmota_si7021_humidity(section: Mapping[str, Any]) -> DiscoveryResult:
    si7021 = section.get("StatusSNS", {}).get("SI7021", {})
    if isinstance(si7021, dict) and "Humidity" in si7021:
        yield Service(item="Humidity")


# -------- Check: SI7021 --------


def check_tasmota_si7021_temperature(
    item: str,
    params: TempParamType,
    section: Mapping[str, Any],
) -> CheckResult:
    si7021 = section.get("StatusSNS", {}).get("SI7021", {})
    if "Temperature" not in si7021:
        yield Result(state=State.UNKNOWN, summary=f"{item}: no data")
        return
    value = float(si7021["Temperature"])
    yield from check_temperature(value, params, value_store=get_value_store(), unique_name=item)


def check_tasmota_si7021_dewpoint(
    item: str,
    params: TempParamType,
    section: Mapping[str, Any],
) -> CheckResult:
    si7021 = section.get("StatusSNS", {}).get("SI7021", {})
    if "DewPoint" not in si7021:
        yield Result(state=State.UNKNOWN, summary=f"{item}: no data")
        return
    value = float(si7021["DewPoint"])
    yield from check_temperature(value, params, value_store=get_value_store(), unique_name=item)


def check_tasmota_si7021_humidity(
    item: str,
    params: Mapping[str, Any],
    section: Mapping[str, Any],
) -> CheckResult:
    si7021 = section.get("StatusSNS", {}).get("SI7021", {})
    if "Humidity" not in si7021:
        yield Result(state=State.UNKNOWN, summary=f"{item}: no data")
        return
    value = float(si7021["Humidity"])
    yield from check_humidity(value, params)


# -------- CheckPlugins Registration --------


check_plugin_tasmota_si7021_temperature = CheckPlugin(
    name="tasmota_si7021_temperature",
    sections=["tasmota_status"],
    service_name="SI7021 %s",
    discovery_function=discover_tasmota_si7021_temperature,
    check_function=check_tasmota_si7021_temperature,
    check_ruleset_name="temperature",
    check_default_parameters={},
)

check_plugin_tasmota_si7021_dewpoint = CheckPlugin(
    name="tasmota_si7021_dewpoint",
    sections=["tasmota_status"],
    service_name="SI7021 %s",
    discovery_function=discover_tasmota_si7021_dewpoint,
    check_function=check_tasmota_si7021_dewpoint,
    check_ruleset_name="temperature",
    check_default_parameters={},
)

check_plugin_tasmota_si7021_humidity = CheckPlugin(
    name="tasmota_si7021_humidity",
    sections=["tasmota_status"],
    service_name="SI7021 %s",
    discovery_function=discover_tasmota_si7021_humidity,
    check_function=check_tasmota_si7021_humidity,
    check_ruleset_name="humidity",
    check_default_parameters={},
)
