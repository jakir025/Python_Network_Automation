from napalm import get_network_driver
driver = get_network_driver('ios')
device = driver('192.168.184.141','jakir','Hoss1234')
device.open()

#device.load_merge_candidate(filename='30_cisco_backup')
device.load_replace_candidate(filename='30_cisco_backup')
print (device.compare_config()) 

if len(device.compare_config()) > 0:
    choice = input("\nWould you like to replace the config? [YN]: ")
    if choice == 'y':
        print('commit...')
        device.commit_config()
        choice = input("\nWould you like to rollback the previous config? [YN]: ")
        if choice == 'y':
            print('committing..')
            device.rollback()
    else:
        print('Discarding')
        device.discard_config()  

else:
    print('NO DIFFERENCE')      

#close the session with the device
device.close()
print('Done.')
     


