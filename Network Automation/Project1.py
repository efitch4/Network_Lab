import paramiko

# Define device parameters
device = {
    'hostname': '192.168.122.100',  # IP address of the Docker container
    'username': 'eric',              # SSH username
    'password': 'Sickness18!',       # SSH password
}

# SSH into the device and retrieve configuration
try:
    # Create SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the device
    client.connect(**device)

    # Send command to retrieve configuration
    stdin, stdout, stderr = client.exec_command('show running-config')
    print(stdout.read().decode())

    # Close the SSH connection
    client.close()

except Exception as e:
    print(f"An error occurred: {e}")
