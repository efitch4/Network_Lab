import paramiko
import time


def execute_commands(hostname, username, password, commands, ssh_err=None):
    try:
        print(f"Connecting to the device {hostname}...")
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=hostname, port=22, username=username ,password=password)

        print(f"Connected to to the device {hostname}")
        remote_conn = ssh_client.invoke_shell()

        #Send commands

        for command in commands:
            remote_conn.send(command + '\n')
            time.sleep(1) # Wait for command to execute
            output = remote_conn.recv(65535).decode()
            print(output, end='')

        ssh_client.close()
    except paramiko.AuthenticaionException:
        print("Authentication failed , check credentials")
    except paramiko.SSHException as ssh_err:
        print(f"Unable to establish SSH connection: {ssh_err}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
        
# Define the device details and commands
hostname = '192.168.204.138'
username = 'admin'
password = 'admin'
commands = ['config t', 'int lo1001', 'ip address 1.1.1.1 255.255.255.0','end']

# Execute commands
execute_commands(hostname, username,password,commands)