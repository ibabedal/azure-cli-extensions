# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long
from azure.cli.core.commands import CliCommandType
#from azext_disk_expand._client_factory import cf_disk_expand


def load_command_table(self, _):

    # TODO: Add command type here
    # disk_expand_sdk = CliCommandType(
    #    operations_tmpl='<PATH>.operations#None.{}',
    #    client_factory=cf_disk_expand)


    with self.command_group('vm disk') as g:
        g.custom_command('expand', 'expand')
        # g.command('delete', 'delete')
        #g.custom_command('list', 'list_disk_expand')
        # g.show_command('show', 'get')
        # g.generic_update_command('update', setter_name='update', custom_func_name='update_disk_expand')


    #with self.command_group('disk_expand', is_preview=True):
    #    pass

