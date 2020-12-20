# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long

from knack.arguments import CLIArgumentType
#from azure.cli.core.commands.parameters import get_resource_name_completion_list
#from azure.cli.core.commands.parameters import tags_type

def load_arguments(self, _):

    with self.argument_context('vm disk expand') as c:
        c.argument('name',options_list=['--name','-n'] ,help='Name of the VM you want to expand its disk')
        c.argument('resource-group',options_list=['--resource-group','-g'] ,help='Name of the resource group of the VM you want to expand its disk')
        c.argument('osdisk',options_list=['--os-disk'] ,help='Selecting OS disk ofthe VM to expand')
        c.argument('newsize',options_list=['--new-size'] ,help='Select new size of the disk in Gigabyte')

