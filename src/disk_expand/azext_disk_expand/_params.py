# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long

from knack.arguments import CLIArgumentType
from azure.cli.core.commands.parameters import get_resource_name_completion_list

def load_arguments(self, _):

    from azure.cli.core.commands.parameters import tags_type
    from azure.cli.core.commands.validators import get_default_location_from_resource_group

    # REUSABLE ARGUMENT DEFINITIONS
    name_arg_type = CLIArgumentType(options_list=['--name', '-n'], metavar='NAME')
    existing_vm_name = CLIArgumentType(overrides=name_arg_type,
                                       configured_default='vm',
                                       help="The name of the Virtual Machine. You can configure the default using `az configure --defaults vm=<name>`",
                                       completer=get_resource_name_completion_list('Microsoft.Compute/virtualMachines'), id_part='name')

    disk_expand_name_type = CLIArgumentType(options_list='--disk-expand-name-name', help='Name of the Disk_expand.', id_part='name')

    with self.argument_context('vm disk expand') as c:
    c.argument('vm_name', existing_vm_name)





    with self.argument_context('disk_expand') as c:
        c.argument('tags', tags_type)
        c.argument('location', validator=get_default_location_from_resource_group)
        c.argument('disk_expand_name', disk_expand_name_type, options_list=['--name', '-n'])

    with self.argument_context('disk_expand list') as c:
        c.argument('disk_expand_name', disk_expand_name_type, id_part=None)
