import logging
from sys import exit
from textwrap import dedent

# Base class for all tasks
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
            current_task = self.task_map_next_task(next_task_name)

            # Ensure the last task is executed 
            current_task.execute()

# Task to demonstrate string manipulation
class StringManipulation(Task):
    def execute(self):
        text = "Python Study Drill"
        print(dedent(f"""
            Original text: {text}
            Lowercase: {text.lower()}
            Uppercase: {text.upper()}
            Reversed: {text[::-1]}
        """))
        return 'conditional_logic'
    
# Task to demonstrate conditional logic
class ConditionalLogic(Task):
    def execute(self):
        num = 7
        if num > 5:
            result = "greater than 5"
        elif num == 5:
            result = "equal to 5"
        else:
            result = "less than 5"

        print(f"Number {num} is {result}.")
        return 'loop_operations'
    
# Task to demonstrate loop operations
class LoopOperations(Task):
    def execute(self):
        result = 0 
        for i in range(1, 6):
            result += i
            print(f"Adding {i}, total: {result}")

            return 'file_handling'
        
# Task to demonstrate file handling
class FileHandling(Task):
    def execute(self):
        file_name = "study_drill.txt"
        content = "This is a Python  study drill file."

        with open(file_name, "w") as file:
            file.write(content)

            print(f"File '{file_name}' created with content: {content}")
            return 'class_inheritance'
        
# Task to demonstrate class inheritance 
class ClassInheritance(Task):
    def execute(self):
        # Base class
        class Animal: 
            def sound(self):
                return"Some generic sound"
            
        # Derived class
        class Dog(Animal):
                def sound(self):
                    return "Bark"
        
        my_dog = Dog()
        print(f"The dog says: {my_dog.sound()}")
        return 'error_handling'
    
 # Task to demonstrate error handling
class ErrorHandling(Task):
    def execute(self):
        try:
            result = 10/0
        except ZeroDivisionError as e:
            print(f"Error occured: {e}")
        finally:
            print("This block always executes")

        return 'logging_demo'
    
# Task to demonstrate logging
class LoggingDemo(Task):
    def execute(self):
        logging.info("Loggin is setup correctly")
        print("Logging completed. Check the log file.")
        return 'complete'
    
#Placeholder for final completion state
class Complete(Task):
    def execute(self):
        logging.info("Logging is setup correctly.")
        print("Logging completed. Check the log file")
        return 'complete'

# Map class to manage task transitions 
class TaskMap(object):
    tasks = {
        'string_manipulation': StringManipulation(),
        'conditional_logic': ConditionalLogic(),
        'loop_operations': LoopOperations(),
        'file_Handling': FileHandling(),
        'class_inheritance': ClassInheritance(),
        'error_handling': ErrorHandling(),
        'logging_demo': LoggingDemo(),
        'complete': Complete(),
    }

    def __init__(self, start_task):
        self.start_task = start_task

    def next_task(self, task_name):
        return TaskMap.tasks.get(task_name)
    
    def initial_task(self):
        return self.next_task(self.start_task)
    
 # Setup logging 
logging.basicConfig(filename= 'study_drill.log', level=logging.INFO, format = '%(asctime)s -%(levelname)s -%(message)s')

# Start the study drill
task_map = TaskMap('string_manuipulation')
task_engine = Engine(task_map)
task_engine.run()













