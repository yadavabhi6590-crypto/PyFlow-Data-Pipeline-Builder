

import os
from pyflow.utils import load_config

if __name__ == "__main__":
    print("__Debugging Path ___")
    print("Current Working Directory:",os.getcwd())
    print("--- Question 1: Config Parser Test ---")
    print("Key 'Config/config.yaml' exist karrta hai ", os.path.exists("config/config.yaml"))



try:
    config = load_config("config/config.yaml")
    
    print("\n[SUCCESS] Config file successfully load ho gayi!")
    print("Output Dictionary:", config)
    print("Project Name:", config.get("project_name"))
except Exception as e:
    print(f"[Error]:{e}")




from pyflow.utils import load_config, ConfigurationError,PyFlowError


if __name__=="__main__":
    print("--Question 2: Customer Exception test--")


try:
    print("Testing with worng config path...")
    load_config("config/galat_file.yaml")

except ConfigurationError as ce:
    print(f"\n[SUCCESS]Caught Expected Custom ConfigurationError:\n->{ce}")

except PyFlowError as pe:
    print(f"\n[Success] Caught General PyFlowError: \n->{pe}")