from napalm import get_network_driver
driver = get_network_driver('ios')
device = driver('192.168.184.141','jakir','Hoss1234')
device.open()

device.load_merge_candidate(filename='29_cisco_route')
#device.load_replace_candidate(filename='29_cisco_route')
print (device.compare_config())

# choice = input("\nWould you like to commit? [YN]: ")
# if choice == 'y':
#     print('commit...')
#     device.commit_config()

# else:
#     print('Discarding')
#     device.discard_config()   

if len(device.compare_config()) > 0:
    choice = input("\nWould you like to commit? [YN]: ")
    if choice == 'y':
        print('commit...')
        device.commit_config()

    else:
        print('Discarding')
        device.discard_config()  

else:
    print('NO DIFFERENCE')      

#close the session with the device
device.close()
print('Done.')
     


