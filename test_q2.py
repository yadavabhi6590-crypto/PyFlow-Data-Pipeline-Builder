from pyflow.utils import load_config, ConfigurationError, PyFlowError
from pyflow.utils import load_config

if __name__ == "__main__":
    print("--- Question 2: Custom Exception Test ---")
    
    try:
        print("Testing with wrong config path...")
        load_config("config/galat_file.yaml")
        
    except ConfigurationError as ce:
        print(f"\n[SUCCESS] Caught Expected Custom ConfigurationError:\n-> {ce}")
        
    except PyFlowError as pe:
        print(f"\n[SUCCESS] Caught General PyFlowError:\n-> {pe}")