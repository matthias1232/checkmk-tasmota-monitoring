#!/usr/bin/env python3

# Beispiel-Agent-Output (nur Dokumentation, wird NICHT geparst):
# <<<check_mk>>>
# Version: Tasmota Special Agent 1.0
# AgentOS: linux
# <<<tasmota_status:sep(0)>>>
# {"Status":{"Module":0,"DeviceName":"bath-hmd-temp","FriendlyName":["bath-hmd-temp"],"Topic":"tasmota_BAEBDC","ButtonTopic":"0","Power":"0","PowerLock":"0","PowerOnState":3,"LedState":1,"LedMask":"FFFF","SaveData":1,"SaveState":1,"SwitchTopic":"0","SwitchMode":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"ButtonRetain":0,"SwitchRetain":0,"SensorRetain":0,"PowerRetain":0,"InfoRetain":0,"StateRetain":0,"StatusRetain":0},"StatusPRM":{"Baudrate":115200,"SerialConfig":"8N1","GroupTopic":"tasmotas","OtaUrl":"http://ota.tasmota.com/tasmota32/release/tasmota32.bin","RestartReason":"Software reset CPU","Uptime":"1T07:25:12","StartupUTC":"2025-11-21T13:44:37","Sleep":50,"CfgHolder":4617,"BootCount":12,"BCResetTime":"2025-11-18T15:38:13","SaveCount":45},"StatusFWR":{"Version":"15.1.0(release-tasmota32)","BuildDateTime":"2025-10-11T13:05:13","Core":"3_3_0","SDK":"5.3.4.250826","CpuFrequency":160,"Hardware":"ESP32-PICO-D4 v1.1","CR":"431/699"},"StatusLOG":{"SerialLog":2,"WebLog":2,"MqttLog":0,"FileLog":0,"SysLog":0,"LogHost":"","LogPort":514,"SSId":["Manias-IoT",""],"TelePeriod":15,"Resolution":"558180C0","SetOption":["00008009","2805C80001000600003C5A0A192800000000","00000080","00006000","00004000","00000000"]},"StatusMEM":{"ProgramSize":2082,"Free":797,"Heap":147,"StackLowMark":3,"PsrMax":0,"PsrFree":0,"ProgramFlashSize":4096,"FlashSize":4096,"FlashChipId":"1640C8","FlashFrequency":40,"FlashMode":"DIO","Features":["0809","9F9AD7DF","0015A001","B7F7BFCF","05DA9BC4","E0360DC7","480840D2","20200000","D4BC482D","810A80F1","00000814"],"Drivers":"1,2,!3,4,5,7,!8,9,10,11,12,!14,!16,!17,!20,!21,!24,26,!27,29,!34,!35,38,50,52,!59,!60,62,!63,!66,!67,!68,!73,!75,82,!86,!87,!88,!91,!121","Sensors":"1,2,3,5,6,7,8,9,10,11,12,13,14,15,17,18,19,20,21,22,26,31,34,37,39,40,42,43,45,51,52,55,56,58,59,64,66,67,74,85,92,95,98,103,105,109,127","I2CDriver":"7,8,9,10,11,12,13,14,15,17,18,20,24,29,31,36,41,42,44,46,48,58,62,65,69,76,77,82,89"},"StatusNET":{"Hostname":"tasmota-BAEBDC-3036","IPAddress":"192.168.56.210","Gateway":"192.168.56.1","Subnetmask":"255.255.255.0","DNSServer1":"192.168.56.1","DNSServer2":"dd87:3344:5566:2::1","Mac":"F0:24:F9:BA:EB:DC","IP6Global":"dd87:3344:5566:2:f224:f9ff:feba:ebdc","IP6Local":"fe80::f224:f9ff:feba:ebdc%st2","Ethernet":{"Hostname":"","IPAddress":"0.0.0.0","Gateway":"0.0.0.0","Subnetmask":"0.0.0.0","DNSServer1":"192.168.56.1","DNSServer2":"dd87:3344:5566:2::1","Mac":"00:00:00:00:00:00","IP6Global":"","IP6Local":""},"Webserver":2,"HTTP_API":1,"WifiConfig":4,"WifiPower":16.0},"StatusMQT":{"MqttHost":"192.168.56.2","MqttPort":1883,"MqttClientMask":"DVES_%06X","MqttClient":"DVES_BAEBDC","MqttUser":"openhabian","MqttCount":4,"MqttTLS":0,"MAX_PACKET_SIZE":1200,"KEEPALIVE":30,"SOCKET_TIMEOUT":4},"StatusTIM":{"UTC":"2025-11-22T21:09:49Z","Local":"2025-11-22T22:09:49","StartDST":"2025-03-30T02:00:00","EndDST":"2025-10-26T03:00:00","Timezone":"+01:00","Sunrise":"08:10","Sunset":"17:01"},"StatusSNS":{"Time":"2025-11-22T22:09:49","SHT3X":{"Temperature":23.0,"Humidity":52.3,"DewPoint":12.7},"TempUnit":"C"},"StatusSTS":{"Time":"2025-11-22T22:09:49","Uptime":"1T07:25:12","UptimeSec":113112,"Heap":144,"SleepMode":"Dynamic","Sleep":50,"LoadAvg":25,"MqttCount":4,"Berry":{"HeapUsed":4,"Objects":51},"POWER":"OFF","Dimmer":0,"Color":"000000","HSBColor":"0,0,0","Channel":[0,0,0],"Scheme":0,"Width":1,"Fade":"OFF","Speed":1,"LedTable":"ON","Wifi":{"AP":1,"SSId":"Manias-IoT","BSSId":"D8:07:B6:4F:25:9D","Channel":11,"Mode":"HT40","RSSI":92,"Signal":-54,"LinkCount":1,"Downtime":"0T00:00:03"},"Hostname":"tasmota-BAEBDC-3036","IPAddress":"192.168.56.210"}}
from collections.abc import Mapping
from datetime import datetime
from enum import Enum
from typing import cast, Literal, TypedDict, TypeVar
from xml.etree import ElementTree

from pydantic import BaseModel

from cmk.agent_based.v1 import check_levels as check_levels_v1
from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    get_value_store,
    Metric,
    render,
    Result,
    Service,
    State,
    StringTable,
)
from cmk.plugins.lib.memory import check_element
from cmk.plugins.lib.temperature import check_temperature, TempParamType
from cmk.plugins.lib.humidity import check_humidity, CheckParams

import json
from collections.abc import Mapping
from typing import Any
from cmk.plugins.lib.temperature import check_temperature, TempParamType
from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    get_value_store,
    CheckResult,
    DiscoveryResult,
    Service,
    Result,
    State,
    StringTable,
    Metric
)

# -------- Discovery: SHT3X --------


def discover_tasmota_sht3x_temperature(section: Mapping[str, Any]) -> DiscoveryResult:
    sht3x = section.get("StatusSNS", {}).get("SHT3X", {})
    if isinstance(sht3x, dict):
        if "Temperature" in sht3x:
            yield Service(item="Temperature")
            
def discover_tasmota_sht3x_dewpoint(section: Mapping[str, Any]) -> DiscoveryResult:
    sht3x = section.get("StatusSNS", {}).get("SHT3X", {})
    if isinstance(sht3x, dict):
        if "DewPoint" in sht3x:
            yield Service(item="DewPoint")

def discover_tasmota_sht3x_humidity(section: Mapping[str, Any]) -> DiscoveryResult:
    sht3x = section.get("StatusSNS", {}).get("SHT3X", {})
    if isinstance(sht3x, dict):
        if "Humidity" in sht3x:
            yield Service(item="Humidity")

# -------- Check: SHT3X --------


def check_tasmota_sht3x_temperature(
    item: str,
    params: TempParamType,
    section: Mapping[str, Any],
) -> CheckResult:
    sht3x = section.get("StatusSNS", {}).get("SHT3X", {})
    if "Temperature" not in sht3x:
        yield Result(state=State.UNKNOWN, summary=f"{item}: no data"); return
    value = float(sht3x["Temperature"])
    yield from check_temperature(value, params, value_store=get_value_store(), unique_name=item)
    
def check_tasmota_sht3x_dewpoint(
    item: str,
    params: TempParamType,
    section: Mapping[str, Any],
) -> CheckResult:
    sht3x = section.get("StatusSNS", {}).get("SHT3X", {})
    if "DewPoint" not in sht3x:
        yield Result(state=State.UNKNOWN, summary=f"{item}: no data"); return
    value = float(sht3x["DewPoint"])
    yield from check_temperature(value, params, value_store=get_value_store(), unique_name=item)


def check_tasmota_sht3x_humidity(
    item: str,
    params: Mapping[str, Any],
    section: Mapping[str, Any],
) -> CheckResult:
    sht3x = section.get("StatusSNS", {}).get("SHT3X", {})
    unit = "%"
    if "Humidity" not in sht3x:
        yield Result(state=State.UNKNOWN, summary=f"{item}: no data"); return
    value = float(sht3x["Humidity"])
    if value:
        yield from check_humidity(float(value), params, )



# -------- CheckPlugins Registration --------
    

check_plugin_tasmota_sht3x_temperature = CheckPlugin(
    name="tasmota_sht3x_temperature",
    sections=["tasmota_status"],
    service_name="SHT3X %s",
    discovery_function=discover_tasmota_sht3x_temperature,
    check_function=check_tasmota_sht3x_temperature,
    check_ruleset_name="temperature",
    check_default_parameters={},
)

check_plugin_tasmota_sht3x_dewpoint = CheckPlugin(
    name="tasmota_sht3x_dewpoint",
    sections=["tasmota_status"],
    service_name="SHT3X %s",
    discovery_function=discover_tasmota_sht3x_dewpoint,
    check_function=check_tasmota_sht3x_dewpoint,
    check_ruleset_name="temperature",
    check_default_parameters={},
)

check_plugin_tasmota_sht3x_humidity = CheckPlugin(
    name="tasmota_sht3x_humidity",
    sections=["tasmota_status"],
    service_name="SHT3X %s",
    discovery_function=discover_tasmota_sht3x_humidity,
    check_function=check_tasmota_sht3x_humidity,
    check_ruleset_name="humidity",
    check_default_parameters={},
)














