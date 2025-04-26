from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command, netmiko_send_config
from nornir_utils.plugins.functions import print_result
import os




def backup_config(task):
    # This will backup the running config
    result = task.run(
        task=netmiko_send_command,
        command_string="show running-config"
    )

    # Save to a local file
    with open (f"{task.host}.txt", "w") as backup_file:
        backup_file.write(result.result)

def verify_config(task):
    # Verify specific config (e.g., NTP server)
    check_result = task.run(
        task=netmiko_send_command,
        command_string="show run | include ntp server"    
    )
    if "ntp server 192.168.1.100" not in check_result.result:
        task.run(
            task=netmiko_send_config,
            config_commands=["ntp server 192.168.1.100"]
        )

def main():
    nr = InitNornir(config_file="C:/Users/Eric/OneDrive/Desktop/pypro/projects/config.yaml")
    print("Step 1: Backing up configuration...")
    backup_results = nr.run(task=backup_config)
    print_result(backup_results)

    print("Step 2: Verifying and applying configuration...")
    verify_results = nr.run(task=verify_config)
    print_result(verify_results)

if __name__ =="__main__":
    main()