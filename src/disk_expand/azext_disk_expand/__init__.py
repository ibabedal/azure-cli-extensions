# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core import AzCommandsLoader

from azext_disk_expand._help import helps  # pylint: disable=unused-import


class DiskexpandCommandsLoader(AzCommandsLoader):

    def __init__(self, cli_ctx=None):
        from azure.cli.core.commands import CliCommandType
        from azext_disk_expand._client_factory import cf_disk_expand
        disk_expand_custom = CliCommandType(
            operations_tmpl='azext_disk_expand.custom#{}',
            client_factory=cf_disk_expand)
        super(DiskexpandCommandsLoader, self).__init__(cli_ctx=cli_ctx,
                                                  custom_command_type=disk_expand_custom)

    def load_command_table(self, args):
        from azext_disk_expand.commands import load_command_table
        load_command_table(self, args)
        return self.command_table

    def load_arguments(self, command):
        from azext_disk_expand._params import load_arguments
        load_arguments(self, command)


COMMAND_LOADER_CLS = DiskexpandCommandsLoader
