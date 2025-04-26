from sys import exit
from netmiko import ConnectHandler
from textwrap import dedent 
import logging


#Base class for all network tasks
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
            current_task = self.task_map.initial_task
            last_task = self.task_map.next_task('complete')

            while current_task != last_task:
                next_task_name = current_task.execute()
                current_task = self.task_map.next_task(next_task_name)

                #Ensure the last task is executed
                current_task.execute()

# Example subclass repersenting a failure state
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
            'host':'192.168.1.1',
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
class CheckDeviceReachablity(Task):