from netmiko import ConnectHandler
from datetime import datetime

# Device connection parameters
device = {
    'device_type': 'cisco_ios',
    'host': '192.168.1.172', # IP address of your router
    'username': 'admin',
    'password': 'admin',
}

# Establish SSH connection to the router 
connection = ConnectHandler(**device)

#Get the running configuration
running_config = connection.send_command("show running-config)")

# Generate a filename based on the current date and time
backup_filename = f"r1_running_config{datetime.now().strftime('%Ym%d_%H%M%S')}.txt"

#write the running configuration to a file
with open(backup_filename, "w") as backup_file:
    backup_file.write(running_config)

print(f"Backup of the running configuration saved to {backup_filename}")

#Close the connection
connection.disconnect()