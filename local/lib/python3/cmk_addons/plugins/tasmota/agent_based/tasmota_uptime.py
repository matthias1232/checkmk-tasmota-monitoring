#!/usr/bin/env python3

# Beispiel-Agent-Output (nur Dokumentation, wird NICHT geparst):
# <<<check_mk>>>
# Version: Tasmota Special Agent 1.0
# AgentOS: linux
# <<<tasmota_status:sep(0)>>>
# {"Status":{...},"StatusSTS":{"Time":"2025-11-22T22:09:49","Uptime":"1T07:25:12","UptimeSec":113112,...}}

from collections.abc import Mapping
from typing import Any

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Service,
)
from cmk.plugins.lib import uptime


# -------- Discovery --------

def discover_tasmota_uptime(section: Mapping[str, Any]) -> DiscoveryResult:
    """Discover uptime service if UptimeSec is present in Tasmota data."""
    if section.get("StatusSTS", {}).get("UptimeSec") is not None:
        yield Service()


# -------- Check --------

def check_tasmota_uptime(params: Mapping[str, Any], section: Mapping[str, Any]) -> CheckResult:
    """Check Tasmota uptime by converting to uptime.Section and using uptime.check."""
    try:
        uptime_sec = section.get("StatusSTS", {}).get("UptimeSec")
        if uptime_sec is None:
            return
        
        # Convert to uptime.Section and use the standard uptime check function
        uptime_section = uptime.Section(uptime_sec=float(uptime_sec), message=None)
        yield from uptime.check(params, uptime_section)
    except (KeyError, ValueError, TypeError):
        return


# -------- Check Plugin --------

check_plugin_tasmota_uptime = CheckPlugin(
    name="tasmota_uptime",
    sections=["tasmota_status"],
    service_name="Uptime",
    discovery_function=discover_tasmota_uptime,
    check_function=check_tasmota_uptime,
    check_default_parameters={},
    check_ruleset_name="uptime",
)
