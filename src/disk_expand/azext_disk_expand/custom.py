# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from multiprocessing import Pool
from datetime import datetime

from knack.util import CLIError
from knack.log import get_logger

from azext_disk_expand.cli_utils import run_cli_command, prepare_cli_command

logger = get_logger(__name__)

def expand(cmd, resource_group_name, name, newsize, osdisk=True):
    print('We will do a needed checks before start the operation !')
    ## Collecting VM profile 
    try:
        #removing G from the new size value
        newsize = newsize[:-1]
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
                    #checking if new size is greater than old size , else drop an exception
                    if int(newsize) <= int(disk_current_size):
                        raise CLIError('Your new disk size: '+ str(newsize) +'G is less than current size: '+ str(disk_current_size)+ 'G ')
                    
                    else:

                        #starting the job
                        print()
                        print('We have done with our checkes, below is the information we collected : ')
                        print('VM name : {}'.format(name))
                        print('Image urn : {0}:{1}:{2}:{3}'.format(vm_image_publisher,vm_image_offer,vm_image_sku,vm_image_exactVersion) )
                        print('OS disk name : {0} which is in resource group : {1}'.format(disk_name,disk_rg_name))
                        print('Current disk size : {}G'.format(disk_current_size))
                        print('New disk size : {}G'.format(newsize))
                        print('-----------------------')

                        print()
                        print('Stopping the VM')
                        stop_cli_cmd = prepare_cli_command(['vm','deallocate','-n',name,'-g',resource_group_name])
                        run_cli_command(stop_cli_cmd)
                        print('VM now stopped, taking a snapshot of the OS disk before doing any changes and it will be with same resource group as disk ....')
                        dateTimeObj = datetime.now()
                        timestampStr = dateTimeObj.strftime('%d-%m-%YT%H-%M')
                        snapshot_name = name+'-snapshot-'+timestampStr
                        snapshot_cli_cmd = prepare_cli_command(['snapshot','create','-g',disk_rg_name,'-n',snapshot_name,'--source',vm_os_disk_id])
                        snapshot_cli_output = run_cli_command(snapshot_cli_cmd,return_as_json=True)
                        print('We have created a snapshot named {0} in resource group {1}'.format(snapshot_cli_output['name'],snapshot_cli_output['resourceGroup']))
                        print('Expanding disk now ...')
                        
                        
                        disk_expand_cli_cmd = prepare_cli_command(['disk','update','--ids',vm_os_disk_id,'--size-gb',newsize])
                        disk_expand_output = run_cli_command(disk_expand_cli_cmd,return_as_json=True)
                        print('Done expanding the disk , starting the VM now ....')
                        vm_start_cli_cmd = prepare_cli_command(['vm','start','-n',name,'-g',resource_group_name])
                        run_cli_command(vm_start_cli_cmd)
                        print('VM started, executing the script for expanding disk from OS ...')

                        #starting with CSE part, we will deploy test script for now.
                        script_url = 'https://raw.githubusercontent.com/ibabedal/test/main/test.sh'
                        command_to_execute = script_url.split('/')[-1]
                        protected_settings = '{ "fileUris" : [ "'+script_url+'" ] , "commandToExecute" : "./' +command_to_execute +'" }'

                        extension_cli_cmd = prepare_cli_command(['vm','extension','set',
                                                                '--resource-group',resource_group_name,'--vm-name',name,
                                                                '--name','customScript',
                                                                '--publisher','Microsoft.Azure.Extensions',
                                                                '--protected-settings',protected_settings
                                                                    ])
                        extension_cli_output = run_cli_command(extension_cli_cmd,return_as_json=True)

                        print('We are done, you may do a final reboot for checking .....')




    except Exception as e:
        print(e)


