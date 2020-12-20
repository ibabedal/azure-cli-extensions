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
        vm_info_cmd = prepare_cli_command(['vm','get-instance-view','-n',name,'-g',resource_group_name])
        vm_info_output= run_cli_command(vm_info_cmd,return_as_json=True)
        vm_id = vm_info_output['id']
        vm_powerstate = str(vm_info_output['instanceView']['statuses'][1]['code']).split('/')[1]
        vm_os_disk_id = vm_info_output['storageProfile']['osDisk']['managedDisk']['id']

            #check if VM is running or not, as we need it running to check the agent status
        if vm_powerstate != 'running': 
            raise CLIError('Error : Please make sure the VM is started as we need to check the VM agent')
        else:
            # check if agent is running as it is needed for CSE 
            vm_agent = vm_info_output['instanceView']['vmAgent']['statuses'][0]['displayStatus']
            vm_agent_version = vm_info_output['instanceView']['vmAgent']['vmAgentVersion']
            if vm_agent != 'ready' and vm_agent_version == 'Unknown' :
                raise CLIError('Error: VM is running, but agnet not running or not installed, please make sure to have it installed and in ready state')
            else:
                # check if it is market place image 
                # to get more enhanced and to confirm if it is endorsed distribution
                endorsed_publishers = ['RedHat','SUSE','Canonical','OpenLogic','Oracle','Credativ']
                vm_image_publisher = vm_info_output['storageProfile']['imageReference']['publisher']
                vm_image_offer = vm_info_output['storageProfile']['imageReference']['offer']
                vm_image_sku = vm_info_output['storageProfile']['imageReference']['sku']
                vm_image_exactVersion = vm_info_output['storageProfile']['imageReference']['exactVersion']
                if vm_image_publisher not in endorsed_publishers :
                    raise CLIError('Error: Apologies, but our current version supports only VMs from endorsed marketplace publishers')
                else:
                    vm_osName = vm_info_output['instanceView']['osName']
                    vm_osVersion = vm_info_output['instanceView']['osVersion']
                    disk_info_cmd = prepare_cli_command(['disk','show','--ids',vm_os_disk_id])
                    disk_info_output = run_cli_command(disk_info_cmd,return_as_json=True)
                    disk_name = disk_info_output['name']
                    disk_rg_name = disk_info_output['resourceGroup']
                    disk_current_size = disk_info_output['diskSizeGb']
                    #starting the job
                    print('We have done with our checkes, below is the information we collected : ')
                    print('VM name : {}'.format(name))
                    print('Image urn : {0}:{1}:{2}:{3}'.format(vm_image_publisher,vm_image_offer,vm_image_sku,vm_image_exactVersion) )
                    print('OS disk name : {0} which is in resource group : {1}'.format(disk_name,disk_rg_name))
                    print('Current disk size : {}G'.format(disk_current_size))
                    print('New disk size : {}'.format(newsize))
                    print('-----------------------')
                    print('Start with stopping the VM')
                    stop_cli_cmd = prepare_cli_command(['vm','stop','-n',name,'-g',resource_group_name])
                    



    except Exception as e:
        print(e)


        



    #except Exception as e :
    #    print(e)
    #    raise CLIError('TODO: Implement `disk_expand create`')
