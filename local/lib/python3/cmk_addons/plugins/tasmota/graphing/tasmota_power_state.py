#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Checkmk Graphing plugin: Tasmota Power Switch State Metric
#

from cmk.graphing.v1 import graphs, metrics, Title, perfometers

# -------- Metrics --------

metric_power_state = metrics.Metric(
    name="power_state",
    title=Title("Power Switch State"),
    unit=metrics.Unit(metrics.DecimalNotation("")),
    color=metrics.Color.GREEN,
)

# -------- Graphs --------

graph_tasmota_power_state = graphs.Graph(
    name="tasmota_power_state",
    title=Title("Power Switch State"),
    simple_lines=[
        "power_state",
    ],
)

# -------- Perfometers --------

perfometer_tasmota_power_state = perfometers.Perfometer(
    name="tasmota_power_state",
    focus_range=perfometers.FocusRange(
        perfometers.Closed(0),
        perfometers.Closed(1),
    ),
    segments=["power_state"],
)
