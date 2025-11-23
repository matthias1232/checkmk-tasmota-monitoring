#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Checkmk Graphing plugin: Tasmota Power/Energy Sensor Metrics
#

from cmk.graphing.v1 import graphs, metrics, Title, perfometers

# -------- Metrics --------

metric_power = metrics.Metric(
    name="power",
    title=Title("Power"),
    unit=metrics.Unit(metrics.DecimalNotation("W")),
    color=metrics.Color.BLUE,
)

metric_current = metrics.Metric(
    name="current",
    title=Title("Current"),
    unit=metrics.Unit(metrics.DecimalNotation("A")),
    color=metrics.Color.GREEN,
)

metric_apparent_power = metrics.Metric(
    name="apparent_power",
    title=Title("Apparent Power"),
    unit=metrics.Unit(metrics.DecimalNotation("VA")),
    color=metrics.Color.PURPLE,
)

metric_reactive_power = metrics.Metric(
    name="reactive_power",
    title=Title("Reactive Power"),
    unit=metrics.Unit(metrics.DecimalNotation("VAr")),
    color=metrics.Color.ORANGE,
)

metric_power_factor = metrics.Metric(
    name="power_factor",
    title=Title("Power Factor"),
    unit=metrics.Unit(metrics.DecimalNotation("")),
    color=metrics.Color.CYAN,
)

metric_energy_today_kwh = metrics.Metric(
    name="energy_today_kwh",
    title=Title("Energy Today"),
    unit=metrics.Unit(metrics.DecimalNotation("kWh")),
    color=metrics.Color.LIGHT_BLUE,
)

metric_energy_yesterday_kwh = metrics.Metric(
    name="energy_yesterday_kwh",
    title=Title("Energy Yesterday"),
    unit=metrics.Unit(metrics.DecimalNotation("kWh")),
    color=metrics.Color.LIGHT_GRAY,
)

metric_energy_total_kwh = metrics.Metric(
    name="energy_total_kwh",
    title=Title("Energy Total"),
    unit=metrics.Unit(metrics.DecimalNotation("kWh")),
    color=metrics.Color.DARK_BLUE,
)

# -------- Graphs --------

graph_tasmota_power = graphs.Graph(
    name="tasmota_power",
    title=Title("Real Power"),
    simple_lines=[
        "power",
    ],
)

graph_tasmota_apparent_power = graphs.Graph(
    name="tasmota_apparent_power",
    title=Title("Apparent Power"),
    simple_lines=[
        "apparent_power",
    ],
)

graph_tasmota_reactive_power = graphs.Graph(
    name="tasmota_reactive_power",
    title=Title("Reactive Power"),
    simple_lines=[
        "reactive_power",
    ],
)

graph_tasmota_energy = graphs.Graph(
    name="tasmota_energy",
    title=Title("Energy Usage"),
    simple_lines=[
        "energy_today_kwh",
        "energy_yesterday_kwh",
    ],
)

graph_tasmota_current = graphs.Graph(
    name="tasmota_current",
    title=Title("Current"),
    simple_lines=[
        "current",
    ],
)

graph_tasmota_power_factor = graphs.Graph(
    name="tasmota_power_factor",
    title=Title("Power Factor"),
    simple_lines=[
        "power_factor",
    ],
)

# -------- Perfometers --------

perfometer_tasmota_power = perfometers.Perfometer(
    name="tasmota_power",
    focus_range=perfometers.FocusRange(
        perfometers.Closed(0),
        perfometers.Open(1000),
    ),
    segments=["power"],
)
