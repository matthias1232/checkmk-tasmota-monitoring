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


from collections.abc import Iterable, Mapping, Sequence

from cmk.server_side_calls.v1 import (
    HostConfig,
    noop_parser,
    replace_macros,
    Secret,
    SpecialAgentCommand,
    SpecialAgentConfig,
)


def _agent_tasmota_arguments(
    params: Mapping[str, object],
    hostconfig: HostConfig,
) -> Iterable[SpecialAgentCommand]:


    args = []
    
    args += ["-H", hostconfig.name]
    args += ["-password", params['password']]

    yield SpecialAgentCommand(command_arguments=args)


special_agent_tasmota = SpecialAgentConfig(
    name="tasmota",
    parameter_parser=noop_parser,
    commands_function=_agent_tasmota_arguments,
)