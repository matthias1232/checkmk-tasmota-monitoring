#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Checkmk Ruleset: Tasmota Firmware Check
#

from cmk.rulesets.v1 import Help, Label, Title
from cmk.rulesets.v1.form_specs import (
    BooleanChoice,
    DefaultValue,
    DictElement,
    Dictionary,
    SingleChoice,
    SingleChoiceElement,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, Topic


def _firmware_parameter_form() -> Dictionary:
    return Dictionary(
        elements={
            "disable_online_check": DictElement(
                parameter_form=BooleanChoice(
                    title=Title("Disable online firmware check"),
                    label=Label("Do not check GitHub for latest firmware version"),
                    help_text=Help(
                        "When enabled, the check will not query GitHub API for the latest "
                        "firmware version and will always report OK. Only the current firmware "
                        "version will be displayed."
                    ),
                ),
                required=False,
            ),
            "outdated_state": DictElement(
                parameter_form=SingleChoice(
                    title=Title("State when firmware is outdated"),
                    help_text=Help(
                        "Select the monitoring state to report when a newer firmware version "
                        "is available on GitHub."
                    ),
                    elements=[
                        SingleChoiceElement(name="ok", title=Title("OK")),
                        SingleChoiceElement(name="warn", title=Title("WARN")),
                        SingleChoiceElement(name="crit", title=Title("CRIT")),
                    ],
                    prefill=DefaultValue("warn"),
                ),
                required=False,
            ),
        },
        title=Title("Tasmota Firmware Check"),
        help_text=Help(
            "Configure how the Tasmota firmware check should behave when checking "
            "for firmware updates."
        ),
    )


rule_spec_tasmota_firmware = CheckParameters(
    name="tasmota_firmware",
    title=Title("Tasmota Firmware"),
    topic=Topic.APPLICATIONS,
    parameter_form=_firmware_parameter_form,
    condition=None,
)
