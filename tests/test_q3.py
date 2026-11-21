import time
from pyflow.utils import timing_decorator, load_config

@timing_decorator

def sample_heavy_task(seconds: int):
    print(f"Task is runging....{seconds} this seconds will stop")
    time.sleep(seconds)
    print("Function Khatam ho gaya!")
    return "Done Successfully"

if __name__ =="__main__":
    print("__Question 3 : Timing Decorator test-----")

    # then we will check owe custom decorator 
    result=sample_heavy_task(2)
    print(f"Result returned: {result}")