from netmiko import ConnectHandler

# Switch details
switch = {
    "device_type": "cisco_ios",
    "ip": "192.168.1.10",  # Replace with your switch's IP
    "username": "admin",    # Replace with your username
    "password": "admin",    # Replace with your password
    "secret": "admin",      # Replace with your enable password
}

# VLAN Configuration Commands
vlans = [
    {"id": 10, "name": "HR"},
    {"id": 20, "name": "Finance"},
    {"id": 30, "name": "IT"}
]

interface_vlan_mapping = {
    "GigabitEthernet0/1": 10,
    "GigabitEthernet0/2": 20,
    "GigabitEthernet0/3": 30
}

def configure_vlans():
    try:
        print("Connecting to the switch...")
        connection = ConnectHandler(**switch)

        # Enter enable mode
        connection.enable()

        print("Creating VLANs...")
        vlan_commands = []
        for vlan in vlans:
            vlan_commands.append(f"vlan {vlan['id']}")
            vlan_commands.append(f"name {vlan['name']}")
        
        # Send VLAN configuration commands
        connection.send_config_set(vlan_commands)

        print("Assigning VLANs to interfaces...")
        interface_commands = []
        for interface, vlan_id in interface_vlan_mapping.items():
            interface_commands.append(f"interface {interface}")
            interface_commands.append(f"switchport mode access")
            interface_commands.append(f"switchport access vlan {vlan_id}")
        
        # Send interface VLAN mapping commands
        connection.send_config_set(interface_commands)

        print("Verifying VLAN configuration...")
        vlan_output = connection.send_command("show vlan brief")
        print(vlan_output)

        print("Verifying interface configuration...")
        interface_output = connection.send_command("show running-config | include interface|switchport access vlan")
        print(interface_output)

        # Disconnect
        connection.disconnect()
        print("Disconnected from the switch.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    configure_vlans()
