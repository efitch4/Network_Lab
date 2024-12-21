from paramiko import client
from getpass import getpass
import time

linux_cmd = ['ls -larth', 'echo $USER', 'hostname', 'sdfsad']
cisco_cmd = ['show ver']

def exec_cmd_executor(hostname, commands, username, password):
    print(f"Connected to the device {hostname}...")
    ssh_client = client.SSHClient()
    ssh_client.set_missing_host_key_policy(client.AutoAddPolicy())
    ssh_client.connect(hostname=hostname, port=22, username=username, password=password, look_for_keys=False,
                       allow_agent=False)
    # Invoke shell opens an interactive ssh shell and executes the command
    print(f"Connected to the device{hostname}")

    for cmd in commands:
        print(f"\n{'#' * 10} Executing {cmd}{'#' * 10}")
        stdin, stdout, stderr = ssh_client.exec_command(cmd)
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            print(f"Error Occurred: {err}")


exec_cmd_executor('192.168.204.130', linux_cmd, 'eric', 'Sickness18!')
exec_cmd_executor('192.168.204.134', cisco_cmd, 'admin', 'admin')
