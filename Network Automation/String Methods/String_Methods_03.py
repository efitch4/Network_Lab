import sys
import time
import traceback
from paramiko import client, ssh_exception
from getpass import getpass
import socket
import datetime

with open('show_commands.txt', 'r') as conf_file:
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
        device_access = ssh_client.invoke_shell()
        device_access.send("terminal len 0\n")

        for index, cmd in enumerate(commands, start=1):
            timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
            cmd = cmd.strip().replace(' ', '_')
            file_name = f"{timestamp}_{str(index).zfill(2)}_{cmd}.txt"
            with open(file_name, 'w') as cmd_data:
                device_access.send(f"{cmd}\n")
                time.sleep(1)
                output = device_access.recv(65535)
                cmd_data.write(output.decode())
                print(output.decode(), end='')

    except ssh_exception.NoValidConnectionsError:
        print("SSH Port not reachable")
    except socket.gaierror:
        print("Check the hostname")
    except ssh_exception.AuthenticationException:
        print("Authentication failed, check credentials")

    except:
        print("Exception Occurred")
        print(sys.exc_info())
        # traceback.print_exception(*sys.exc_info())


cisco_cmd_executor('192.168.204.138', new_cmd, 'admin', 'admin')
