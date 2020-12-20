# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.help_files import helps  # pylint: disable=unused-import


helps['vm disk expand'] = """
    type: group
    short-summary: Use to expand disks attached to a Linux VM
    examples:
        - name: Expand OS disk for the VM
          text: >
            az vm disk expand --name myVM --resource-group myRG --os-disk --new-size 100G
"""

# helps['disk_expand delete'] = """
#     type: command
#     short-summary: Delete a Disk_expand.
# """

# helps['disk_expand show'] = """
#     type: command
#     short-summary: Show details of a Disk_expand.
# """

# helps['disk_expand update'] = """
#     type: command
#     short-summary: Update a Disk_expand.
# """
