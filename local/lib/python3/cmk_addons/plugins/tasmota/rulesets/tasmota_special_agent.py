#!/usr/bin/env python3


#This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the #License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU #General Public License for more details.
#
#You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# Written by Matthias Binder, November 2025
# https://github.com/matthias1232
#
# License: GNU General Public License

from collections.abc import Mapping

from cmk.rulesets.v1 import Help, Label, Title
from cmk.rulesets.v1.form_specs import (
    BooleanChoice,
    DefaultValue,
    DictElement,
    Dictionary,
    Integer,
    List,
    migrate_to_password,
    MultipleChoice,
    MultipleChoiceElement,
    Password,
    SingleChoice,
    SingleChoiceElement,
    String,
    FixedValue,
    validators,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange, NetworkPort
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic

def _parameter_form() -> Dictionary:
    return Dictionary(
        elements={
            "password": DictElement(
                parameter_form=Password(
                    title=Title("Web Interface Password (optional but highly recommended)"),
                    custom_validate=(validators.LengthInRange(min_value=1),),
                    migrate=migrate_to_password,
                ),
                required=False,
            ),
        },
        title=Title("Tasmota Special Agent"),
        help_text=Help("Configure the Tasmota Special Agent to monitor Tasmota devices"),
    )


rule_spec_special_agent_tasmota = SpecialAgent(
    name="tasmota",
    title=Title("Tasmota Devices"),
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form,
)