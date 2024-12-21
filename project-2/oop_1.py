from sys import exit
from netmiko import ConnectHandler
from textwrap import dedent

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
        # Print a failure message and exit
        print("Task failed. Exiting.")
        exit(1)

# Example of a more complex task with decision branches
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
            Attempting to connect to the device...
        """))

        try:
            connection = ConnectHandler(**device)
            print("Connection established.")
            return 'check_running_config'
        except Exception as e:
            print(f"Connection failed: {e}")
            return 'failure'

# Example of a task to verify running configuration
class CheckRunningConfig(Task):
    def execute(self):
        device = {
            'device_type': 'cisco_ios',
            'host': '192.168.1.1',
            'username': 'admin',
            'password': 'admin',
        }

        print(dedent("""
            Retrieving running configuration...
        """))

        connection = ConnectHandler(**device)
        running_config = connection.send_command("show running-config")

        # Example check within the configuration
        if 'interface GigabitEthernet0/1' in running_config:
            print("Required configuration present.")
            return 'save_config'
        else:
            print("Configuration missing. Task failed.")
            return 'failure'

# Task to save the running configuration
class SaveConfig(Task):
    def execute(self):
        device = {
            'device_type': 'cisco_ios',
            'host': '192.168.1.1',
            'username': 'admin',
            'password': 'admin',
        }

        print(dedent("""
            Saving running configuration to startup configuration...
        """))

        connection = ConnectHandler(**device)
        connection.send_command("write memory")
        print("Configuration saved successfully.")
        return 'complete'

# Placeholder for final completion state
class Complete(Task):
    def execute(self):
        print("All tasks completed successfully.")
        return 'complete'

# Map class to manage task transitions
class TaskMap(object):
    tasks = {
        'verify_connection': VerifyConnection(),
        'check_running_config': CheckRunningConfig(),
        'save_config': SaveConfig(),
        'failure': Failure(),
        'complete': Complete(),
    }

    def __init__(self, start_task):
        self.start_task = start_task

    def next_task(self, task_name):
        return TaskMap.tasks.get(task_name)
    
    def initial_task(self):
        return self.next_task(self.start_task)

# Start the task automation
task_map = TaskMap('verify_connection')
task_engine = Engine(task_map)
task_engine.run()
