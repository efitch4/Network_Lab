#Test
from paramiko import client 
from getpass import getpass
import time


hostname = 'router1'

username = input("Enter Username:")

if not username:
    username = 'admin'
    print(f"No username provided, consdering default username {username}")

password =  getpass(f"Enter Password of the user {username}: ") or "admin"

ssh_client = client.SSHClient()
ssh_client.set_missing_host_key_policy(client.AutoAddPolicy)
ssh_client.connect(hostname=hostname,
                   port=22,
                   username=username,
                   password=password,
                   look_for_keys=False,allow_agent=False)
print("Connected succesesfully")
device_access = ssh_client.invoke_shell()
device_access.send("terminal len 0\n")
device_access.send("show run\n")
time.sleep(5)




output = device_access.recv(65535)
print(output.decode())
#print(type(output))
ssh_client.close

## This is a test