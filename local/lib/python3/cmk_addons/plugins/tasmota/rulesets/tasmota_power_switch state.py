#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Checkmk Ruleset: Tasmota Power Switch State Check
#

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    SingleChoice,
    SingleChoiceElement,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, Topic


def _power_state_parameter_form() -> Dictionary:
    return Dictionary(
        elements={
            "expected_state": DictElement(
                parameter_form=SingleChoice(
                    title=Title("Expected power state"),
                    help_text=Help(
                        "Select the expected power state for this device. "
                        "The check will compare the actual state with this expected state."
                    ),
                    elements=[
                        SingleChoiceElement(name="ON", title=Title("ON - Device should be powered on")),
                        SingleChoiceElement(name="OFF", title=Title("OFF - Device should be powered off")),
                    ],
                    prefill=DefaultValue("ON"),
                ),
                required=True,
            ),
            "state_on_mismatch": DictElement(
                parameter_form=SingleChoice(
                    title=Title("State when power state doesn't match expected"),
                    help_text=Help(
                        "Select the monitoring state to report when the actual power state "
                        "does not match the expected state."
                    ),
                    elements=[
                        SingleChoiceElement(name="ok", title=Title("OK - No alert")),
                        SingleChoiceElement(name="warn", title=Title("WARN - Warning")),
                        SingleChoiceElement(name="crit", title=Title("CRIT - Critical")),
                    ],
                    prefill=DefaultValue("warn"),
                ),
                required=True,
            ),
        },
        title=Title("Tasmota Power Switch State"),
        help_text=Help(
            "Configure the expected power state for Tasmota devices and how to alert "
            "when the actual state differs from the expected state."
        ),
    )


rule_spec_tasmota_power_state = CheckParameters(
    name="tasmota_power_state",
    title=Title("Tasmota Power Switch State"),
    topic=Topic.APPLICATIONS,
    parameter_form=_power_state_parameter_form,
    condition=None,
)
