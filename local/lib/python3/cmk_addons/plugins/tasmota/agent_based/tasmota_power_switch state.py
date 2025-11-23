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

# -------- Check Plugin: Power Switch State --------

def discover_tasmota_power_state(section: Mapping[str, Any]) -> DiscoveryResult:
    """Discover if the device has a POWER state in StatusSTS"""
    if "StatusSTS" in section and "POWER" in section["StatusSTS"]:
        yield Service()

def check_tasmota_power_state(params: Mapping[str, Any], section: Mapping[str, Any]) -> CheckResult:
    """Check the current power switch state (ON/OFF)"""
    power_state = section["StatusSTS"]["POWER"]
    expected_state = params.get("expected_state", "ON")
    state_on_mismatch = params.get("state_on_mismatch", "warn")
    
    # Determine the state based on expected vs actual
    if power_state == expected_state:
        state = State.OK
        summary = f"Power is {power_state}"
    else:
        # Map string to State enum
        state_mapping = {
            "ok": State.OK,
            "warn": State.WARN,
            "crit": State.CRIT,
        }
        state = state_mapping.get(state_on_mismatch, State.WARN)
        summary = f"Power is {power_state} (expected: {expected_state})"
    
    yield Result(state=state, summary=summary)
    
    # Add a metric: 1 for ON, 0 for OFF
    power_numeric = 1 if power_state == "ON" else 0
    yield Metric("power_state", power_numeric)

default_power_state_parameters = {
    "expected_state": "ON",
    "state_on_mismatch": "warn",
}

check_plugin_tasmota_power_state = CheckPlugin(
    name="tasmota_power_state",
    sections=["tasmota_status"],
    service_name="Power Switch State",
    discovery_function=discover_tasmota_power_state,
    check_function=check_tasmota_power_state,
    check_ruleset_name="tasmota_power_state",
    check_default_parameters=default_power_state_parameters,
)
