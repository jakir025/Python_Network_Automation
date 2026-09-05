from netmiko import ConnectHandler
from getpass import getpass

#password = getpass('Enter password')

# 2. Used getpass() so you don't hardcode sensitive passwords
RTR_10 = {
    'device_type': 'cisco_ios',
    'ip':        '192.168.184.141',
    'username':    'jakir',
    'password':  getpass('Enter Password'),
}

config_commands = [ 
    'interface loopback0',
    'ip address 111.111.111.111 255.255.255.255',
    'no shutdown'
]

# Using 'with' handles connection setup and breakdown safely
with ConnectHandler(**RTR_10) as net_connect:
    # Sends configuration commands (Netmiko handles config t / exit automatically)
    config_output = net_connect.send_config_set(config_commands)
    print("--- Configuration Output ---")
    print(config_output)
    
    # Sends operational verification command
    show_output = net_connect.send_command('show spanning-tree')
    print("\n--- Show Command Output ---")
    print(show_output)
