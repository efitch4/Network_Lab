import sys
import time
from paramiko import client, ssh_exception
import socket
import datetime

def cisco_cmd_executor(hostname, commands, username, password):
    try:
        print(f"Connecting to the device {hostname}..")
        now = datetime.datetime.now().replace(microsecond=0)
        current_conf_file = f"{now.strftime('%Y-%m-%d_%H-%M-%S')}_{hostname}.txt"
        ssh_client = client.SSHClient()
        ssh_client.set_missing_host_key_policy(client.AutoAddPolicy())
        ssh_client.connect(hostname=hostname, port=22, username=username, password=password, look_for_keys=False,
                           allow_agent=False)

        print(f"Connected to the device {hostname}")
        device_access = ssh_client.invoke_shell()
        device_access.send("terminal len 0\n")
        with open(current_conf_file, 'w') as cmd_data:
            for cmd in commands:
                device_access.send(f"{cmd}")
                time.sleep(1)
                output = device_access.recv(65535)
                cmd_data.write(output.decode())
                print(output.decode(), end='')
        ssh_client.close()
    except ssh_exception.NoValidConnectionsError:
        print("SSH Port not reachable")
    except socket.gaierror:
        print("Check the hostname")
    except ssh_exception.AuthenticationException:
        print("Authentication failed, check credentials")
    except Exception as e:
        print("Exception Occurred:", e)

# Your existing code
with open('show_commands.txt', 'r') as conf_file:
    new_cmd = conf_file.readlines()

cisco_cmd_executor('192.168.204.138', new_cmd, 'admin', 'admin')
