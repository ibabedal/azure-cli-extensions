# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.util import CLIError


def create_disk_expand(cmd, resource_group_name, disk_expand_name, location=None, tags=None):
    raise CLIError('TODO: Implement `disk_expand create`')


def list_disk_expand(cmd, resource_group_name=None):
    raise CLIError('TODO: Implement `disk_expand list`')


def update_disk_expand(cmd, instance, tags=None):
    with cmd.update_context(instance) as c:
        c.set_param('tags', tags)
    return instance