#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Checkmk Agent-based plugin: Tasmota Firmware
#

from collections.abc import Mapping
from typing import Any

import requests  # für GitHub API

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    State,
)


# -------- Helper: GitHub API with Caching --------

import time
import os
from pathlib import Path

# Cache file location (dynamic based on OMD site)
_sitename = os.environ.get("OMD_SITE", "monitoring")
CACHE_FILE = Path(f"/opt/omd/sites/{_sitename}/tmp/check_mk/tasmota_latest_version.cache")
CACHE_DURATION = 12 * 3600  # 12 hours (twice a day)


def get_latest_tasmota_version() -> str | None:
    """Fetch latest Tasmota release tag from GitHub API with caching (12h TTL)."""
    
    # Try to read from cache first
    try:
        if CACHE_FILE.exists():
            cache_age = time.time() - CACHE_FILE.stat().st_mtime
            if cache_age < CACHE_DURATION:
                # Cache is still valid
                cached_version = CACHE_FILE.read_text().strip()
                if cached_version:
                    return cached_version
    except Exception:
        pass  # If cache read fails, fetch from API
    
    # Fetch from GitHub API
    url = "https://api.github.com/repos/arendst/Tasmota/releases/latest"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        latest_version = data.get("tag_name")  # e.g., "v15.1.0"
        
        # Write to cache
        if latest_version:
            try:
                CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
                CACHE_FILE.write_text(latest_version)
            except Exception:
                pass  # If cache write fails, just continue
        
        return latest_version
    except Exception:
        # If API call fails, try to return stale cache if available
        try:
            if CACHE_FILE.exists():
                return CACHE_FILE.read_text().strip()
        except Exception:
            pass
        return None


# -------- Discovery --------

def discover_tasmota_firmware(section: Mapping[str, Any]) -> DiscoveryResult:
    """Discover firmware service if firmware info is present in Tasmota data."""
    if section.get("StatusFWR", {}).get("Version"):
        yield Service()


# -------- Check --------

def check_tasmota_firmware(params: Mapping[str, Any], section: Mapping[str, Any]) -> CheckResult:
    """Check Tasmota firmware version and OTA URL, compare with latest release."""
    try:
        status_fwr = section.get("StatusFWR", {})
        status_prm = section.get("StatusPRM", {})

        version = status_fwr.get("Version")
        ####debug test### version = "15.0.0(release-tasmota32)"

        build_date = status_fwr.get("BuildDateTime")
        ota_url = status_prm.get("OtaUrl")

        if not version:
            yield Result(state=State.UNKNOWN, summary="No firmware version found")
            return

        # Check if online check is disabled
        disable_online_check = params.get("disable_online_check", False)
        
        if disable_online_check:
            # Just show current version without checking GitHub
            summary = f"Version: {version}"
            if build_date:
                summary += f", Build: {build_date}"
            summary += f", online firmware update check disabled"
            yield Result(state=State.OK, summary=summary)
        else:
            # Check GitHub for latest version
            latest = get_latest_tasmota_version()
            
            # Get configured state for outdated firmware (default: warn)
            outdated_state_name = params.get("outdated_state", "warn")
            state_mapping = {
                "ok": State.OK,
                "warn": State.WARN,
                "crit": State.CRIT,
            }
            outdated_state = state_mapping.get(outdated_state_name, State.WARN)

            # Compare with latest release version
            if latest and version.startswith(latest.lstrip("v")):
                state = State.OK
                summary = f"Firmware up-to-date: {version}"
            elif latest:
                state = outdated_state
                summary = f"Firmware outdated: {version}, latest is {latest}"
            else:
                state = State.UNKNOWN
                summary = f"Firmware version: {version} (could not fetch latest release)"

            if build_date:
                summary += f", Build: {build_date}"

            yield Result(state=state, summary=summary)

        # OTA URL as detail
        if ota_url:
            yield Result(state=State.OK, notice=f"OTA URL: {ota_url}")

    except (KeyError, ValueError, TypeError) as e:
        yield Result(state=State.UNKNOWN, summary=f"Error parsing firmware data: {e}")


# -------- Check Plugin --------

check_plugin_tasmota_firmware = CheckPlugin(
    name="tasmota_firmware",
    sections=["tasmota_status"],
    service_name="Firmware",
    discovery_function=discover_tasmota_firmware,
    check_function=check_tasmota_firmware,
    check_default_parameters={
        "disable_online_check": False,
        "outdated_state": "warn",
    },
    check_ruleset_name="tasmota_firmware",
)

