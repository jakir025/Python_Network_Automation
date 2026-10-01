from napalm import get_network_driver
driver = get_network_driver('nxos')
device = driver('192.168.184.145','jakir','Hoss1234')
device.open()

device.load_merge_candidate(filename='32_nexus_route')
#device.load_replace_candidate(filename='32_nexus_backup')
print (device.compare_config()) 

if len(device.compare_config()) > 0:
    choice = input("\nWould you like to replace the config? [YN]: ")
    if choice == 'y':
        print('commit...')
        device.commit_config()

    choice = input("\nWould you like to rollback to the previous config? [YN]: ")
    if choice == 'y':
         print('commit...')
         device.rollback()


    else:
        print('Discarding')
        device.discard_config()  

else:
    print('NO DIFFERENCE')      

#close the session with the device
device.close()
print('Done.')
     


