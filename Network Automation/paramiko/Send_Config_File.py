import sys
import time
import traceback
from paramiko import client, ssh_exception
from getpass import getpass
import socket
import datetime

username = 'admin'
password = 'admin'
csr_cmd = ['show run']
with open('C:\\Users\\Eric\\OneDrive\\Desktop\\pypro\\Network Automation\\config1.txt', 'r') as conf_file:
    new_cmd = conf_file.readlines()
print(new_cmd)


def cisco_cmd_executor(hostname, commands, username, password):
    try:
        print(f"Connecting to the device {hostname}..")
        now = datetime.datetime.now().replace(microsecond=0)
        current_conf_file = f"{now}_{hostname}.txt"
        ssh_client = client.SSHClient()
        ssh_client.set_missing_host_key_policy(client.AutoAddPolicy())
        ssh_client.connect(hostname=hostname, port=22, username=username, password=password, look_for_keys=False,
                           allow_agent=False)

        print(f"Connected to the device {hostname}")
        # Start an interactive shell session
        ssh_shell = ssh_client.invoke_shell()

        # Wait for the command prompt to appear
        while not ssh_shell.recv_ready():
            time.sleep(1)

        # Clear any initial output
        ssh_shell.recv(65535)

        # Send each command and wait for the prompt before sending the next command
        with open(current_conf_file, 'w') as cmd_data:
            for cmd in commands:
                ssh_shell.send(cmd + '\n')  # Send the command
                time.sleep(1)
                output = ssh_shell.recv(65535).decode()  # Receive the output
                cmd_data.write(output)
                print(output, end='')

        ssh_client.close()
    except ssh_exception.NoValidConnectionsError:
        print("SSH Port not reachable")
    except socket.gaierror:
        print("Check the hostname")
    except ssh_exception.AuthenticationException:
        print("Authentication failed, check credentials")
    except Exception as e:
        print("Exception Occurred:", e)
        traceback.print_exc()


cisco_cmd_executor('192.168.204.138', new_cmd, 'admin', 'admin')
