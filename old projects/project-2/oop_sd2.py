from sys import exit
from netmiko import ConnectHandler
from textwrap import dedent
import logging

# Base class for all network tasks 
class Task(object):
    def execute(self):
        # Abstract method, to be implemented by subclasses
        print("This task is not yet configured.")
        exit(1)

# Engine to manage the flow of tasks
class Engine(object):
    def __init__(self, task_map):
        self.task_map = task_map

    def run(self):
        current_task = self.task_map.initial_task()
        last_task = self.task_map.next_task('complete')

        while current_task != last_task:
            next_task_name = current_task.execute()
            current_task = self.task_map.next_task(next_task_name)

        # Ensure the last task is executed
        current_task.execute()

# Example subclass representing a failure state
class Failure(Task):
    def execute(self):
        # Log failure and exit
        logging.error("Task failed. Exiting.")
        exit(1)

# Example of a task to establish a connection and verify reachability
class VerifyConnection(Task):
    def execute(self):
        # Device connection parameters
        device = {
            'device_type': 'cisco_ios',
            'host': '192.168.1.1',
            'username': 'admin',
            'password': 'admin',
        }

        print(dedent("""
            Verifying connection...
        """))

        try:
            connection = ConnectHandler(**device)
            print("Connection established.")
            logging.info("Connection established with %s", device['host'])
            return 'check_device_reachability'
        except Exception as e:
            print(f"Connection failed: {e}")
            logging.error("Connection failed with %s: %s", device['host'], e)
            return 'failure'

# Task to check device reachability via ping
class CheckDeviceReachability(Task):
    def execute(self):
        device = {
            'device_type': 'cisco_ios',
            'host': '192.168.1.1',
            'username': 'admin',
            'password': 'admin',
        }

        print(dedent("""
            Checking device reachability...
        """))

        try:
            connection = ConnectHandler(**device)
            output = connection.send_command("ping 8.8.8.8")
            if "!!!" in output:
                print("Device is reachable.")
                logging.info("Device %s is reachable.", device['host'])
                return 'backup_config'
            else:
                print("Device is not reachable.")
                logging.warning("Device %s is not reachable.", device['host'])
                return 'failure'
        except Exception as e:
            print(f"Reachability check failed: {e}")
            logging.error("Reachability check failed with %s: %s", device['host'], e)
            return 'failure'

# Task to backup the current configuration
class BackupConfig(Task):
    def execute(self):
        device = {
            'device_type': 'cisco_ios',
            'host': '192.168.1.1',
            'username': 'admin',
            'password': 'admin',
        }
        print(dedent("""
            Backing up running configuration...
        """))

        try:
            connection = ConnectHandler(**device)
            running_config = connection.send_command("show running-config")
            with open(f"{device['host']}_running_config.txt", "w") as file:
                file.write(running_config)
            print("Configuration backup successful.")
            logging.info("Configuration backup for %s successful.", device['host'])
            return 'apply_config'
        except Exception as e:
            print(f"Configuration backup failed: {e}")
            logging.error("Configuration backup failed with %s: %s", device['host'], e)
            return 'failure'
        
# Task to apply a new configuration
class ApplyConfig(Task):
    def execute(self):
        device = {
            'device_type': 'cisco_ios',
            'host': '192.168.1.1',
            'username': 'admin',
            'password': 'admin',
        }

        new_config_commands = [
            "interface GigabitEthernet0/2",
            "description Configured by automation script",
            "ip address 192.168.2.1 255.255.255.0",
            "no shutdown"
        ]

        print(dedent("""
            Applying new configuration...
        """))

        
        try:
            connection = ConnectHandler(**device)
            connection.send_config_set(new_config_commands)
            print("New configuartion applied successfully.")
            logging.info("New configuration applied to %s", device['host'], e)
        except Exception as e:
            print(f"Configuration application failed: {e}")
            logging.error("Configuartion application failed with %s: %s", device['host'], e)
            return 'rollback_config'
        
        #Task to verify the new configuration
class VerifyConfig(Task):
    def execute(self):
        device = {
            'device_type': 'cisco_ios',
            'host': '192.168.1.1',
            'username':'admin',
            'password': 'admin'
            }

        print(dedent("""
                      Verifying new configuation...
                             """))
        try:
            connection = ConnectHandler(**device)
            running_config = connection.send_command("show running-config")
            if "interface GigabitEthernet0/2" in running_config:
                print("New configuration verified.")
                logging.info("New configuration verifeid on %s", device['host'])
                return 'save_config'
            else:
                print("Configuration verification failed.")
                logging.warning("Configuration verification failed on %s", device['host'])
                return 'rollback_config'
        except Exception as e:
                print(f"Configuration verififcation {e}")
                logging.error("Configuration verification failed with %s: %s", device['host'], e)
                return 'rollback_config'
        
# Task to save the new configuration
class SaveConfig(Task):
    def execute(self):
        device = {
            'device_type': 'cisco_ios',
            'host':'192.168.1.1',
            'username':'admin',
            'password':'admin',
        }

        print(dedent("""
              Saving running configuration to startup configuration...
                     """))
        try:
            connection =ConnectHandler(**device)
            connection.send_command("write memory")
            print("Configuration saved succesffully.")
            logging.info("Configuartion saved successfully on %s", device['host'])
            return 'complete'
        except Exception as e:
            print(f"Configuration save failed {e}")
            logging.error("Configuration save failed with %s: %s", device['host'], e)
            return 'rollback_config'
        
#Task to rollback to the previous configuration
class RollbackConfig(Task):
    def execute(self):
        device = {
            'device_type': 'cisco_ios',
            'host': '192.168.1.1',
            'username': 'admin',
            'password': 'admin'
        }    

        print(dedent("""""
              Rolling back to previous configuration
        """))

        try:
            connection = ConnectHandler(**device)
            with open(f"{device['host']}_running_config.txt", "r") as file:
                old_config = file.read()
            connection.send_config_set(old_config.splitlines())
            print("Rollback successful.")
            logging.info("Rollback to previous configuration on %s was successful.",device['host'])
            return 'failure'
        except Exception as e:
            print(f"Rollback failed: {e}")
            logging.error("Rollback failed with %s: %s", device['host'], e)
            return 'failure'
        
# Placeholder for final completion state
class Complete(Task):
    def execute(self):
        print("All tasks completled successfully.")
        logging.info("All tasks completed successfully.")
        return 'complete'

#Map class to manage task transitions
class TaskMap(object):
    tasks = {
        'verify_connection': VerifyConnection(),
        'check_device_reachability': CheckDeviceReachability,
        'backup_config':BackupConfig(),
        'apply_config': ApplyConfig(),
        'verify_config':VerifyConfig(),
        'save_config': SaveConfig(),
        'rollback_config': RollbackConfig(),
        'failure':Failure(),
        'complete':Complete(),
    
    }

    def __init__(self, start_task):
        self.start_task = start_task

    def next_task(self, task_name):
        return TaskMap.tasks.get(task_name)
    
    def initial_task(self):
        return self.next_task(self.start_task)
    
# Setup logging 
logging.basicConfig(filename='network_automation.log', level=logging.INFO, format='%(asctime)s - %(levelname)s-%(message)s')

#Start the task automation

task_map = TaskMap('verify_connection')
task_engine = Engine(task_map)
task_engine.run()

    