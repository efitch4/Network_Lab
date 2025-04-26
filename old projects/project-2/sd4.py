from netmiko import ConnectHandler

# Device connection parameters
device = {
    'device_type': 'cisco_ios',
    'host': '192.168.1.10',  # The IP address you assigned to the switch
    'username': 'admin',
    'password': 'admin',
}

# Establish SSH connection to the switch
connection = ConnectHandler(**device)

# Example command to check interface status
output = connection.send_command("show ip int brief")
print(output)

# Example of sending additional configuration commands
config_commands = [
    'interface GigabitEthernet0/1',
    'description Connected to server',
    'switchport mode access',
    'switchport access vlan 10',
    'no shutdown'
]
connection.send_config_set(config_commands)
print("Configuration applied.")

# Disconnect the connection
connection.disconnect()
