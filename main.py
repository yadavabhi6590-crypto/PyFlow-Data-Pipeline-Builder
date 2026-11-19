
import pandas as pd
from pyflow.utils import load_config


# load the config file 
config= load_config("config/config.yaml")

csv_path = config["paths"]['input_csv']
print("Data file path found:", csv_path)

# then find the real data in this file

df=pd.read_csv(csv_path)
print("inside the file data")
print(df)