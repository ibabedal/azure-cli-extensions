# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from multiprocessing import Pool

from knack.util import CLIError
from knack.log import get_logger

from azext_disk_expand.cli_utils import run_cli_command, prepare_cli_command

logger = get_logger(__name__)

def expand(cmd, resource_group_name, name, newsize, osdisk=True):
    print('We will do a needed checks before start the operation !')
    ## Collecting VM profile 
    try:
        cli_cmd = prepare_cli_command(['vm','get-instance-view','-n',name,'-g',resource_group_name])
        cmd_output= run_cli_command(cli_cmd,return_as_json=True)
        vm_id = cmd_output['id']
        vm_powerstate = str(cmd_output['instanceView']['statuses'][1]['code']).split('/')[1]
        vm_osName = cmd_output['instanceView']['osName']
        vm_osVersion = cmd_output['instanceView']['osVersion']
        vm_agent = cmd_output['instanceView']['vmAgent']['statuses'][0]['displayStatus']
        vm_agent_version = cmd_output['instanceView']['vmAgent']['vmAgentVersion']
        vm_image_publisher = cmd_output['storageProfile']['imageReference']['publisher']
        vm_image_offer = cmd_output['storageProfile']['imageReference']['offer']
        vm_image_sku = cmd_output['storageProfile']['imageReference']['sku']
        vm_image_exactVersion = cmd_output['storageProfile']['imageReference']['exactVersion']

        #check if VM is running or not, as we need it running to check the agent status
        if vm_powerstate != 'running' : 
                raise CLIError('Please make sure the VM is started as we need to check the VM agent')



    except Exception as e :
        print(e)
        raise CLIError('TODO: Implement `disk_expand create`')
