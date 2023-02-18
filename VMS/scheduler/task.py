import _thread
import micropython
from micropython import schedule
from micropython import const
from utime import sleep_ms

class Task:
    def __init__(self, name, delay_ms=500, priority=1):
        self.name = name
        self.delay_ms = delay_ms
        self.priority = priority
        
        # Start task
        _thread.start_new_thread(self.run, ())

    def run(self):
        while True:
            # Run the task
            self.task()
            
            # Delay the task for the specified number of milliseconds
            sleep_ms(self.delay_ms)
            
    def task(self):
        # LOGIC HERE
        pass
