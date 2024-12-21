import time
from paramiko import client,RSAKey
from getpass import getpass

linux_cmd = ['ls -larth', 'echo $USER', 'hostname', 'sdgf']


def exec_cmd_executor(hostname, commands, username):
    print(f"Connected to the device {hostname}...")
    ssh_client = client.SSHClient()
    ssh_client.set_missing_host_key_policy(client.AutoAddPolicy())
    ssh_client.connect(hostname=hostname, port=22, username=username,
                       look_for_keys=True,
                       allow_agent=True)

    # Invoke shell opens an interactive ssh shell and executes the command
    print(f"Connected to the device{hostname}")

    for cmd in commands:
        print(f"\n{'#' * 10} Executing {cmd}{'#' * 10}")
        stdin, stdout, stderr = ssh_client.exec_command(cmd)
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            print(f"Error Occurred: {err}")


exec_cmd_executor('192.168.204.135', linux_cmd, 'lab2')
