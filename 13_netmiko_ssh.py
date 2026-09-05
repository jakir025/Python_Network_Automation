from netmiko import ConnectHandler


RTR_10= {'device_type':'cisco_ios',
'host':    '192.168.184.141',
'username': 'jakir',
'password':'Hoss1234',}

net_connect=ConnectHandler(**RTR_10)
config_commands = [ 'int lo0',
                   'ip add 111.111.111.111 255.255.255.255',
                   'no shut']

output = net_connect.send_config_set(config_commands)
print(output)
      
output = net_connect.send_command('show spanning-tree')
print(output)