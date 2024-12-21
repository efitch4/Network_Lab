from netmiko import ConnectHandler
from datetime import datetime

# Define the device details
router = {
    "device_type": "cisco_ios",
    "ip": "192.168.1.157",  # Replace with your router's IP
    "username": "admin",    # Replace with your username
    "password": "admin",    # Replace with your password
    "secret": "admin",      # Replace with your enable password if needed
}

# TFTP server details for backup
tftp_server = "192.168.1.100"  # Replace with your TFTP server's IP address
backup_filename = f"router_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.cfg"

try:
    # Connect to the device
    print("Connecting to the router...")
    connection = ConnectHandler(**router)
    connection.enable()

    # Backup the current configuration
    print("Backing up the current configuration...")
    backup_command = f"copy running-config tftp://{tftp_server}/{backup_filename}"
    backup_output = connection.send_command(backup_command, expect_string=r"[confirm]")
    connection.send_command("\n", expect_string=r"#")  # Confirm backup
    print(f"Configuration backed up to {tftp_server} as {backup_filename}")

    # Erase the startup configuration
    print("Erasing startup configuration...")
    erase_output = connection.send_command("write erase", expect_string=r"[confirm]")
    connection.send_command("\n", expect_string=r"#")  # Confirm erase
    print("Startup configuration erased.")

    # Reload the router
    print("Reloading the router...")
    reload_output = connection.send_command("reload", expect_string=r"[confirm]")
    connection.send_command("\n", expect_string=r"#")  # Confirm reload
    print("Router is reloading...")

    # Disconnect from the device
    connection.disconnect()
    print("Disconnected from the router.")

except Exception as e:
    print(f"An error occurred: {e}")
