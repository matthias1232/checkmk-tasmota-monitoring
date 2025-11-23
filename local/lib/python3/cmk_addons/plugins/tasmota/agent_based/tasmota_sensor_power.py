#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Checkmk Agent-based plugin: Tasmota Firmware
#

from collections.abc import Mapping
from typing import Any
from cmk.agent_based.v1 import check_levels as check_levels_v1
import requests  # für GitHub API

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    render,
    State,
    Metric,
)

# -------- Check Plugin: Wattage --------

def discover_tasmota_wattage(section: Mapping[str, Any]) -> DiscoveryResult:
    if "StatusSNS" in section and "ENERGY" in section["StatusSNS"] and "Power" in section["StatusSNS"]["ENERGY"]:
        yield Service()

def check_tasmota_wattage(params: Mapping[str, Any], section: Mapping[str, Any]) -> CheckResult:
    power = section["StatusSNS"]["ENERGY"]["Power"]
    
    # Extract warn/crit thresholds from params
    levels_upper = params.get("levels_abs_upper")  # (warn, crit)
    levels_lower = params.get("levels_abs_lower")  # (warn, crit)
    levels_perc_upper = params.get("levels_perc_upper")
    levels_perc_lower = params.get("levels_perc_lower")
    
    yield from check_levels_v1(
        value=power,
        levels_upper=levels_upper if levels_upper and levels_upper != (0.0, 0.0) else None,
        levels_lower=levels_lower if levels_lower and levels_lower != (0.0, 0.0) else None,
        metric_name="power",
        label="Wattage",
        render_func=lambda x: f"{x} W",
    )
    yield from check_levels_v1(
        value=power / 2000 * 100.0,
        levels_upper=levels_perc_upper if levels_perc_upper and levels_perc_upper != (0.0, 0.0) else None,
        levels_lower=levels_perc_lower if levels_perc_lower and levels_perc_lower != (0.0, 0.0) else None,
        metric_name=None,
        label="Wattage",
        render_func=render.percent,
        notice_only=True,
    )
    if "Today" in section["StatusSNS"]["ENERGY"]:
        energy_today_wh = section["StatusSNS"]["ENERGY"]["Today"]
        energy_today_kwh = energy_today_wh / 1000.0
        yield Metric("energy_today_kwh", energy_today_kwh)
        yield Result(state=State.OK, notice=f"Energy Today: {energy_today_kwh:.2f} kWh")
    if "Yesterday" in section["StatusSNS"]["ENERGY"]:
        energy_yesterday_wh = section["StatusSNS"]["ENERGY"]["Yesterday"]
        energy_yesterday_kwh = energy_yesterday_wh / 1000.0
        yield Metric("energy_yesterday_kwh", energy_yesterday_kwh)
        yield Result(state=State.OK, notice=f"Energy Yesterday: {energy_yesterday_kwh:.2f} kWh")
    if "Total" in section["StatusSNS"]["ENERGY"]:
        energy_total_wh = section["StatusSNS"]["ENERGY"]["Total"]
        energy_total_kwh = energy_total_wh / 1000.0
        yield Metric("energy_total_kwh", energy_total_kwh)
        yield Result(state=State.OK, notice=f"Energy Total: {energy_total_kwh:.2f} kWh")
    if "Current" in section["StatusSNS"]["ENERGY"]:
        current = section["StatusSNS"]["ENERGY"]["Current"]
        yield Metric("current", current)
        yield Result(state=State.OK, notice=f"Current: {current:.2f} A")
    if "ApparentPower" in section["StatusSNS"]["ENERGY"]:
        apparent_power = section["StatusSNS"]["ENERGY"]["ApparentPower"]
        yield Metric("apparent_power", apparent_power)
        yield Result(state=State.OK, notice=f"Apparent Power: {apparent_power:.0f} VA")
    if "ReactivePower" in section["StatusSNS"]["ENERGY"]:
        reactive_power = section["StatusSNS"]["ENERGY"]["ReactivePower"]
        yield Metric("reactive_power", reactive_power)
        yield Result(state=State.OK, notice=f"Reactive Power: {reactive_power:.0f} VAr")
    if "PowerFactor" in section["StatusSNS"]["ENERGY"]:
        power_factor = section["StatusSNS"]["ENERGY"]["PowerFactor"]
        yield Metric("power_factor", power_factor)
        yield Result(state=State.OK, notice=f"Power Factor: {power_factor:.2f}")

        
default_psu_wattage_parameters = {
    "levels_abs_upper": (500.0, 600.0),
    "levels_abs_lower": (0.0, 0.0),
    "levels_perc_upper": (80.0, 90.0),
    "levels_perc_lower": (0.0, 0.0),
}


check_plugin_tasmota_wattage = CheckPlugin(
    name="tasmota_wattage",
    sections=["tasmota_status"],
    service_name="Wattage",
    discovery_function=discover_tasmota_wattage,
    check_function=check_tasmota_wattage,
    check_ruleset_name="psu_wattage",
    check_default_parameters=default_psu_wattage_parameters,
)
