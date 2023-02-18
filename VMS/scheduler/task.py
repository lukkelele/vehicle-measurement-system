import _thread
import micropython
from micropython import schedule
from micropython import const
from utime import sleep_ms

class Task:
    def __init__(self, name, delay_ms, priority):
        # Save the task name, delay, and priority
        self.name = name
        self.delay_ms = delay_ms
        self.priority = priority
        
        # Start the task in a separate thread
        _thread.start_new_thread(self.run, ())

    def run(self):
        while True:
            # Run the task
            self.task()
            
            # Delay the task for the specified number of milliseconds
            sleep_ms(self.delay_ms)
            
    def task(self):
        # Override this method to implement your task logic
        pass

# Define constants
TASK1_NAME = const(1)
TASK1_DELAY_MS = const(1000)
TASK1_PRIORITY = const(1)

TASK2_NAME = const(2)
TASK2_DELAY_MS = const(2000)
TASK2_PRIORITY = const(2)

# Define two tasks that inherit from the Task class
class Task1(Task):
    def task(self):
        print("Task 1 running")

class Task2(Task):
    def task(self):
        print("Task 2 running")

# Start the FreeRTOS scheduler to run the tasks
micropython.schedule(schedule)
