import json
import logging
import os
import yaml

# 1. Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("PyFlowConfigLogger")


# 2. Custom Exception
class PyFlowError(Exception):
    """PyFlow ka main base error."""
    pass


class ConfigurationError(PyFlowError):
    """Jab config file missing ya galat ho tab yeh error aayega."""
    pass
class ExtractionError(PyFlowError):
    pass
class validationError(PyFlowError):
    pass


# 3. Main Config Parser Function
def load_config(config_path: str) -> dict:
    # Check karo ki file computer mein hai bhi ya nahi
    if not os.path.exists(config_path):
        raise ConfigurationError(f"Configuration file nahi mili: {config_path}")

    try:
        # File ko read ('r') mode mein kholo
        with open(config_path, "r", encoding="utf-8") as file:
            lower_path = config_path.lower()

            # Agar file YAML hai
            if lower_path.endswith((".yaml", ".yml")):
                config_data = yaml.safe_load(file)

            # Agar file JSON hai
            elif lower_path.endswith(".json"):
                config_data = json.load(file)

            # Agar koi aur galat format hai (jaise .txt ya .csv)
            else:
                raise ConfigurationError(
                    f"Unsupported format: {config_path}. Sirf .yaml, .yml ya .json use karein."
                )

        # Check karo ki file khali toh nahi thi aur dict hi mila hai
        if not isinstance(config_data, dict):
            raise ConfigurationError(
                f"Config file khali hai ya galat format mein hai: {config_path}"
            )

        logger.info(f"Config successfully load ho gaya: {config_path}")
        return config_data

    except ConfigurationError:
        raise

    except yaml.YAMLError as ye:
        logger.error(f"YAML syntax galat hai {config_path} mein: {ye}")
        raise ConfigurationError(f"Invalid YAML syntax: {ye}") from ye

    except json.JSONDecodeError as je:
        logger.error(f"JSON syntax galat hai {config_path} mein: {je}")
        raise ConfigurationError(f"Invalid JSON syntax: {je}") from je

    except Exception as e:
        logger.error(f"Config load karne mein unexpected error aaya: {e}")
        raise ConfigurationError(f"Failed to load configuration: {e}") from e

#Question 3

import time
from functools import wraps

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        #step 1 Start timer
        start_time = time.perf_counter()
        #step 2 run the real function and save the time
        result = func(*args,  **kwargs)
        #step 3 stop the time and find the total time
        end_time = time.perf_counter()
        execution_time =end_time -start_time
        #step 4 print the time with the help of logger
        logger.info(f"Function '{func.__name__}' took {execution_time:.4f} seconds to execute.")

        #step 5 to return the real function 
        return result
    return wrapper


# Question 4 Generator for large CSV Processing


import csv

def read_csv_in_chunk(file_path: str , chunk_size: int =1000):

    if not os.path.exists(file_path):
        raise ExtractionError(F"CSV file not found at path: {file_path}")
    try:
        # open the file in the read mode
        with open(file_path,'r',encoding='utf-8') as file:
            reader =csv.DictReader(file)
            chunk=[]

            for row in reader:
                chunk.append(row)

                # if the chunk size is complete the yield first
                if len(chunk) == chunk_size:
                    yield chunk
                    chunk=[]

                # if any rows remaining in the last then send it also
                if chunk:
                    yield chunk
    except Exception as e:
        logger.error(f"Error reading CSV in chunks from {file_path}:{e}")
        raise ExtractionError(f"failed to process CSV generator: {e}") from e




from collections import Counter
from typing import Dict, List

    # Q5 Comprehension for Email Domain Analysis .....

def analyze_email_domains(emails: List[str])-> Dict[str, int]:
        """Analyze a list of eamil addresses using comprehension to extract domains and count their frequencies"""

        try:
            # use the list Comperhension to extrect the domain name
            domains = [email.split('@')[1].strip().lower() for email in emails if '@' in email]

            #step 2 Dictionary Comprehension  or counter use them and counting domain
            domain_counts = dict(Counter(domains))
            logger.info(f"Successfully analyzed {len(emails)} email across{len(domain_counts)}unique domains")
            return domain_counts

        except Exception as e:
            logger.error(f"Error during email domain analysis: {e}")
            raise validationError(F"failed to analyze email domains: {e}") from e




#Question 6 Database Connection CPntext manager

import sqlite3
from contextlib import contextmanager

@contextmanager
def db_connection(db_path: str):
    """A context managerfor sfely handling database connections 
    it Automatically commits changes on success, rolls back on error, and closes the 
    connection
    """
    conn =None
    try:
        #step 1 Database as connection joind 
        logger.info(f"Connection to database at: {db_path}")
        conn = sqlite3.connect(db_path)
        # to use the yield that can connection  block inside with
        yield conn
        # if everything is correct then changes will save and (commit) 
        conn.commit()
        logger.info("Database transaction committed successfully.")

    except Exception as e:
        # If any error will ocure on the time of runing then rollback (undo) the work
        if conn:
            conn.rollback()
            logger.error(f"Database error occurred: {e}")
            raise PyFlowError (f"database Operation failed: {e}") from e

    finally:
        # At the end concetion will colse is compulsory 
        if conn:
            conn.close()
            logger.info("Database connection closed safely")



# part b Q1 : Pickup location Frequency using counter

from collections import Counter
import csv
import os
import pandas as pd

def analyze_pickup_locations (file_path:str , top_n: int=5) -> dict:
    """Read the CSv file in chunk and counts the frequency of pickup locations Pulocation
    using collection counter"""

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"taxi parqurt file not found :{file_path}")


    # location_counter = Counter()

    try:
        logger.info(f"Reading Parquet file from :{file_path}")

        df=pd.read_parquet(file_path,columns=["PULocationID"])

        location_counter =Counter(df["PULocationID"].astype(str))

        top_locations=location_counter.most_common(top_n)

        logger.info(f"Top{top_n}Pickup locations analyzed successfully from parquet")
        return dict(top_locations)

    except Exception as e:
        logger.error(f"Error analyzing pickup locations from parquet: {e}")
        raise
        # with open(file_path, "r",encoding='utf-8') as file:
        #     reader = csv.DictReader(file)

        #     for row in reader:
        #     # In texi dataset there is column name is PUlocationId is there
        #     # if column is exist there then put it and insert in this side

        #         pickup_id = row.get('PULocationId') or row.get('pulocationid')
        #         if pickup_id:
        #             location_counter[pickup_id] +=1
        #     # most common(top_n) it's find most frequent locations 

        #         top_locations =location_counter.most_common(top_n)
        #         print(f"Top {top_n} Pickup locations analyzed successfully")
        #         return dict(top_locations)
    except Exception as e:
        print(f"Error analyzing pickup locations :{e}")
        raise


    # Part b Question 2 use defaultdict for hourly fare analysis

from collections import defaultdict
import pandas as pd

def analyze_hourly_fares_parquet(file_path : str)->dict:
        """Analyzes average fare amounts by pickup hour using collections 
        defaultdict"""

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Parquet file not found :{file_path}")

        try:
            logger.info(f"Reading parquet file for hourly fare analyssis :{file_path}")
            df=pd.read_parquet(file_path,columns=['tpep_pickup_datetime',"fare_amount"])
            df["pickup_hour"]=pd.to_datetime(df["tpep_pickup_datetime"]).dt.hour

            #use the difaultdict to create the every fares group
            # key hours values every hours list
            avg_series=df.groupby('pickup_hour')["fare_amount"].mean().round(2)
            avg_hourly_fares=avg_series.to_dict()
            # hourly_fares=defaultdict(list)

            # for _, row in df.iterrows():
            #     hour = int(row['pickup_hour'])
            #     fare = float(row["fare_amount"])
            #     hourly_fares[hour].append(fare)
            # # to find every hours average calculation 
            # avg_hourly_fares={}
            # for hour in sorted (hourly_fares.key()):
            #     fares=hourly_fares[hour]
            #     avg_hourly_fares[hour] = round(sum(fares)/len(fares),2)
            logger.info("Hourly farre analysis completed successfully")
            return avg_hourly_fares

        except Exception as e:
            logger.error(f"Error during hourly fare analysis: {e}")
            raise


#question # rolling buffer
from collections import deque

def calculate_rolling_fare_average(file_path: str, window_size:int=100)->list:

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Parquet file is not found :{file_path}")


    try:
        logger.info(f"Reading parquet file for rolling buffer analysis :{file_path}")

        df=pd.read_parquet(file_path,columns=['fare_amount'])

        buffer=deque(maxlen=window_size)
        rolling_averages=[]

        for fare in df['fare_amount']:
            buffer.append(float(fare))

            # when the buffer is full then find the moving average
            if len(buffer)==window_size:
                avg=sum(buffer)/window_size
                rolling_averages.append(round(avg,2))
        logger.info(f"rolling buffer analysis completed with window size {window_size}")

        return rolling_averages[-10:]

    except Exception as e:
        logger.error(f"Error during rolling buffer analysus:{e}")
        raise





# Question 4 part B

import time


# --- PART B - Q4: List vs Set Performance Benchmark ---
def benchmark_list_vs_set_lookup(file_path: str, sample_size: int = 1000) -> dict:
    """
    Compares the lookup performance (membership test) between a Python list and a set
    using taxi pickup locations from the Parquet file.
    Part B - Question 4.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Parquet file nahi mili: {file_path}")

    try:
        logger.info(f"Reading parquet file for performance benchmark: {file_path}")
        df = pd.read_parquet(file_path, columns=['PULocationID'])
        
        # Data ko list aur set mein convert karte hain
        locations_list = df['PULocationID'].tolist()
        locations_set = set(locations_list)
        
        # Test karne ke liye kuch sample IDs lete hain
        test_items = locations_list[:sample_size]
        
        # 1. List lookup timing (O(N))
        start_time = time.perf_counter()
        for item in test_items:
            _ = item in locations_list
        list_duration = time.perf_counter() - start_time
        
        # 2. Set lookup timing (O(1))
        start_time = time.perf_counter()
        for item in test_items:
            _ = item in locations_set
        set_duration = time.perf_counter() - start_time
        
        logger.info("List vs Set benchmark completed successfully.")
        
        # Keys exact wahi honi chahiye jo test file mein mangi gayi hain
        return {
            "total_records": len(locations_list),
            "sample_lookups": sample_size,
            "list_time_sec": round(list_duration, 6),
            "set_time_sec": round(set_duration, 6),
            "speedup_factor": round(list_duration / set_duration, 2) if set_duration > 0 else 0
        }

    except Exception as e:
        logger.error(f"Error during performance benchmark: {e}")
        raise




class TripRecord:

    def __init__(self, vendor_id, pickup_time, dropoff_time , pu_location ,do_location,fare_amount):
        self.vendor_id =vendor_id
        self.pickup_time=pickup_time
        self.dropoff_time = dropoff_time
        self.pu_location = pu_location
        self.do_location = do_location
        self.fare_amount = fare_amount

    def __eq__(self, other):

        if not isinstance(other,TripRecord):

            return False
        return(
        self.vendor_id == other.vendor_id and
        self.pickup_time == other.pickup_time and
        self.dropoff_time == other.dropoff_time and
        self.pu_location == other.pu_location and
        self.do_location == other.do_location 
    )

    def __hash__(self):
        return hash((
            self.vendor_id,
            self.pickup_time,
            self.dropoff_time,
            self.pu_location,
            self.do_location
        ))

    def  __repr__(self):
        return f"TripRecord(Vendor ={self.vendor_id},Pickup ={self.pickup_time},PU={self.pu_location},Fare=${self.fare_amount})"



def deduplicate_trips_with_class(file_path: str, sample_limit:int = 50000)-> dict:
        """Reads parqute data converts rows into TripRecord objects"""

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Parquet file not found")

        df=pd.read_parquet(file_path,columns=['VendorID',"tpep_pickup_datetime",'tpep_dropoff_datetime','PULocationID','DOLocationID','fare_amount']).head(sample_limit)

        total_row=len(df)
        unique_trip_set =set()

        for _, row in df.iterrows():
            record = TripRecord(
                vendor_id=  row['VendorID'],
                pickup_time= row['tpep_pickup_datetime'],
                dropoff_time= row['tpep_dropoff_datetime'],
                pu_location= row['PULocationID'],
                do_location=row['DOLocationID'],
                fare_amount=row['fare_amount']
            )

            unique_trip_set.add(record)
        unique_count=len(unique_trip_set)
        duplicates_removed= total_row- unique_count

        return{
            "total_processed":total_row,
            "unique_records":unique_count,
            "duplicates_found":duplicates_removed
        }


# Part 1 C CSV chunk processing framework-

def process_large_csv_in_chunks(file_path:  str,chunk_size: int =100000) ->dict:
    """Reads a large CSV file in memory efficient chunks using pandas chunksize
    performs streaming aggregation and return summary statisitics"""

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found :{file_path}")

    try:
        logger.info(f"Starting chunked processing for CSV :{file_path}with chunk size {chunk_size}")
        total_rows=0
        total_fare_sum =0.0
        max_fare =float("-inf")
        min_fare =float("-inf")
        chunk_count =0

        for chunk in pd.read_csv(file_path ,chunksize=chunk_size):
            chunk_count +=1
            rows_in_chunk =len(chunk)
            total_rows += rows_in_chunk

            # If fare_amount are in column then found the streaming state 
            if "Fare_amount" in chunk.columns:
                fares=chunk["fare_amount"].dropna()
                if not fares.empty:
                    total_fare_sum += fares.sum()
                    max_fare =max(max_fare,fares.max())
                    min_fare =min(min_fare,fares.min())

            avg_fare = round(total_fare_sum/total_rows,2) if total_rows>0 else 0.0
            logger.info(f"Successfully processsed {chunk_count} chunk totaling {total_rows:,}rows")

            return{
                "total_chunks_processed":chunk_count,
                "total_rows":total_rows,
                "average_fare":avg_fare,
                "max_fare":round(max_fare,2) if max_fare != float('-inf')else 0.0,
                "min_fare":round(min_fare,2) if min_fare != float('-inf')else 0.0
            }

    except Exception as e:
        logger.error(f"Error during chunked csv processing:{e}")
        raise




 # Part  C-2 automatic file Encoding Detection 

import chardet

def detect_file_encoding(file_path:str,sample_size: int =10000)->dict:
    """Reads the first few bytes of a file in binary mode and users chardet 
    to automatically detect it's character encoding"""

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"file not found :{file_path}")

    try:
        logger.info(f"Detecting encoding for file:{file_path}")

        with open(file_path,'rb') as f:
            raw_data =f.read(sample_size)

        result=chardet.detect(raw_data)
        detected_encoding=result.get('encoding','utf-8')
        confidence=result.get('confidence',0.0)

        logger.info(f"Detected encoding: {detected_encoding}with {confidence *100:.2f}% Confidence.")


        return{
            "encoding":detected_encoding,
            "confidence":round(confidence,2)
        }
    except Exception as e:
        logger.error(f"Error during encoding detection :{e}")
        raise

    def process_csv_with_auto_encoding(file_path: str, chunk_size: int = 50000) -> dict:
    
       """    Automatically detects file encoding first, then processes the CSV in chunks 
      safely without UnicodeDecodeError."""
    # 1. Pehle encoding detect karo
    encoding_info = detect_file_encoding(file_path)
    file_encoding = encoding_info['encoding']
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file nahi mili: {file_path}")

    try:
        logger.info(f"Processing CSV with auto-detected encoding [{file_encoding}]: {file_path}")
        
        total_rows = 0
        chunk_count = 0

        # 2. Detected encoding ke sath chunking run karo
        for chunk in pd.read_csv(file_path, chunksize=chunk_size, encoding=file_encoding, on_bad_lines='skip'):
            chunk_count += 1
            total_rows += len(chunk)

        logger.info(f"Successfully processed {chunk_count} chunks totaling {total_rows:,} rows using encoding: {file_encoding}")
        
        return {
            "detected_encoding": file_encoding,
            "confidence": encoding_info['confidence'],
            "total_chunks": chunk_count,
            "total_rows": total_rows
        }

    except Exception as e:
        logger.error(f"Error reading CSV with encoding {file_encoding}: {e}")
        raise



    # Part c Handling Corrupted CSV files


def process_CSV_with_error_handling(file_path:str,chunk_size: int =50000)->dict:
        """Processes a CSv file in chunk with robust error handling for corrupted rows
        User on_bad_line =skip to bypass malformed records gracefully
        """

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found:{file_path}")

        try:
            logger.info(f"Starting Robust CSV processing with bad line ` handling :{file_path}")

            total_rows =0
            skipped_chunk_or_rows_approx=0
            chunk_count=0

            # on_bad_lines ="skip" se malformed rows skip ho jayengi aur pipeline crash nahi hogi
            #o_bad_line = warn bhi use sakte hai warning ke liye

            for chunk in pd.read_csv(file_path,chunksize= chunk_size,on_bad_lines='skip',low_memory=False):
                chunk_count +=1
                total_rows +=len(chunk)

            logger.info(f"Successfully processed {chunk_count} chunks totaling {total_rows:} Valid rows with error handling")

            return{
                "total_chunks":chunk_count,
                "valid_rows_processes":total_rows,
                "Status":"Success -Corrupted line handled gracefully"
            }

        except pd.errors.ParseError as pe:
            logger.error(f"ParserError encountered :{pe}")
            raise ValueError(f"CSV file structure more corrupted {pe}")
        except Exception as e:
            logger.error(f"Unexpected error during robust CSV processing: {e}")
            raise


# Part C JSON flattening Utility 16

def flatten_json(nested_json:dict,parent_key:str='',sep:str='-')->dict:
    """Recursively Flattens a nested dictionary /json object"""

    items={}
    for k,v in nested_json.items():
        # to create the new key  with parent key 
        new_key= f"{parent_key}{sep}{k}" if parent_key else k

        if isinstance (v,dict):
            # if value is a dictionary then is know as recursive call 
            items.update(flatten_json(v,new_key,sep=sep))

        elif isinstance(v,list):
            # If value is list the index make with flatten
            for i,item in enumerate(v):
                if isinstance(item,dict):
                    items.update(flatten_json(item,f"{new_key}{sep}{i}",sep=sep))
                else:
                    item[f"[new_key]{sep}{i}"]=item
            else:
                items[new_key]=v
        return items

def flatten_json_records(records:list)->pd.DataFrame:
    """Takes a list of nested JSON records flattens each record
    and return a clean pandas dataframe"""

    try:
        logger.info(f"Flattening {len(records)}JSON records")
        flattened_list =[flatten_json(record) for record in records]
        return pd.DataFrame(flattened_list)
    except Exception as e:
        logger.error(f"Error flattening JSON records:{e}")
        raise



import glob

def merge_excel_sheets(file_path:str)->pd.DataFrame:
    """Reads all sheets from a single excel workbook and merges them into a single consolidated pandas Dataframe
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Excel File not found:")

    try:
        logger.info(f"Reading all sheets from excel file: {file_path}")

        sheets_dict = pd.read_excel(file_path,sheet_name=None)

        if not sheets_dict:
            raise ValueError("In excel file there is not found any sheet")

        df_list=[]
        for sheet_name, df in sheets_dict.items():
            #Optional :To track the row from which sheet is loceted
            if df is not None and not df.empty:
                df=df.dropna(how='all').dropna(axis=1,how='all')
                if not df.empty:

                    df['Source_sheet'] =sheet_name
                    logger.info(f"Loaded sheet '{sheet_name} with {len(df)}rows")
                else:
                    logger.warning(f"Sheet '{sheet_name} empty thi")
            else:
                logger.warning(f"Sheet '{sheet_name}' khali (empty) hai, thats why I can skip it.")
        if not df_list:
            raise ValueError("Excel File all sheets are empty  for the concatenate no any thing I can found")
        # To concatenate all the sheets
        master_df=pd.concat(df_list,ignore_index=True,sort=False)

        logger.info(f"Successfully merged {leg(sheets_dict)} sheets.Total rows:{len(master_df):,}")
        return master_df
    except Exception as e:
        logger.error(f"Error merging Excel Sheets :{e}")
        raise


import zipfile
import tarfile

def extract_and_process_archive(archive_path:str,extract_to:str="extracted_data")->list:
    """Extracts compressed files (zip, tar, gz) safely and  returns a list
    of extracted file paths for downstream ETL processing"""

    if not os.path.exists(archive_path):
        raise FileNotFoundError(f"Compressed file not found :{archive_path}")
    # To create the extraction directory if it is not exists
    os.makedirs(extract_to, exist_ok=True)
    extracted_file=[]

    try:
        logger.info(f"Starting extraction for archive :{archive_path}")
        if zipfile.ZipFile(archive_path):
            with zipfile.ZipFile(archive_path,'r') as zip_ref:

                zip_ref.extractall(extract_to)
                extracted_files =[os.path.join(extract_to,name) for name in zip_ref.namelist()]
                logger.info(f"Successfully extracted ZIP archive. Filess:{len(extracted_files)}")

        elif tarfile.is_tarfile(archive_path):
            with tarfile.open(archive_path,'r:*')as tar_ref:
                tar_ref.extractall(extract_to)
                extracted_files=[os.path.join(extract_to,member.name) for member in tar_ref.getmembers()if member.isfile()]
                logger.info(f"Successfully extracted TAR/GZ archive. Files : {len(extracted_files)}")
        else:
            raise ValueError(f"Unsupported or corrupted archive format .files:{len(extracted_files)}")
        return extracted_files
    except Exception as e:
        logger.error(f"Error processing compressed archive :{e}")
        raise


import pyarrow.parquet as pq

# part c 19 
def convert_parquet_to_csv(parquet_path:str, csv_path: str)->dict:
    """Read a parquet file and converts it into a CSV file format
    """

    if not os.path.exists(parquet_path):
        raise FileNotFoundError(f"Parquet file not found:{parquet_path}")
    try:
         logger.info(f"Starting parquet to CSV conversion for :{parquet_path}")

         # step 1 to load the parquet file in pandas dataframe
         df=pd.read_parquet(parquet_path)
         logger.info(f"parquet file successfully read , Total rows :{len(df):,},columns :{len(df.columns)}")

         #step 2 to extracte the file in dataframe
         # index = false means is row number (0,1,2... ) is not save in CSV file
         df.to_csv(csv_path,index=False , encoding='utf-8')

         logger.info(f"Successfully converted Parquet to CSV:{csv_path}")

         return{
             "status":"Success",
             "rows_converted":len(df),
             "columns_count":len(df.columns),
             "output_csv":csv_path
         }
    except Exception as e:
        logger.error(f"Error Converting parquet to csv: {e}")
        raise


 # part C 20 Question 
import time 
import os
import logging
from  watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logging.basicConfig(level=logging.info,format= '%(asctime)s-%(levelname)s-%(message)s')
logger=logging.getLogger("PyflowWatcher")

class PyFlowHandler(FileSystemEventHandler):
    """Custom even Handler that listens to file system changes
    and triggers automated pyflow ETL workflow when new files arrive"""

    def on_created(self,event):
        # If event is any folders(directory) then ignore it, only focuse on files
        if event.is_directory:
            return
        file_path= event.src_path
        logger.info(f"[Trigger]New file is detected :{file_path}")

        # through the file extension decide that which ETL pipeline will run
        self.router_file_to_pipeline(file_path)

    def route_file_to_pipeline(self,file_path):
        ext=os.path.splitext(file_path)[1].lower()
        file_name=os.path.basename(file_path)

        logger.info(f"Analyzing file '{file_path}'with extension {ext}")
        try:
            if ext == '.csv':
                logger.info("-> Routing to CSV Chunk Processor...")
                # Yahan apna PyFlow ka chunked CSV processor call kar sakte ho
                
            elif ext in ['.xlsx', '.xls']:
                logger.info("-> Routing to Excel Sheet Merger...")
                # Yahan apna merge_excel_sheets function call kar sakte ho
                
            elif ext in ['.zip', '.tar', '.gz']:
                logger.info("-> Routing to Archive Extractor...")
                # Yahan apna extract_and_process_archive function call kar sakte ho
                
            elif ext == '.parquet':
                logger.info("-> Routing to Parquet Converter...")
                # Yahan apna parquet-to-csv converter call kar sakte ho
                
            else:
                logger.warning(f"Unsupported file format '{ext}' received. Skipping.")
                
        except Exception as e:
            logger.error(f"Error processing automated file {file_name}: {e}")

def start_file_watcher(watch_directory: str = "data/incoming"):
    """
    Initializes and starts the file system observer on the specified directory.
    """
    if not os.path.exists(watch_directory):
        os.makedirs(watch_directory, exist_ok=True)
        logger.info(f"Directory create kar di hai: {watch_directory}")

    # Event handler ka object banate hain
    event_handler = PyFlowHandler()
    
    # Observer system ka component hai jo background mein folder watch karta hai
    observer = Observer()
    
    # Observer ko batate hain ki kis folder ko watch karna hai aur kaunsa handler use karna hai
    observer.schedule(event_handler, path=watch_directory, recursive=False)
    
    observer.start()
    logger.info(f" PyFlow File Watcher successfully started. Watching folder: '{watch_directory}'")
    logger.info("Press Ctrl + C to stop the watcher.")
    
    try:
        # Infinite loop taaki script background mein chalti rahe aur system band na ho
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Agar user Ctrl+C dabaye toh gracefully watcher ko rok do
        observer.stop()
        logger.info(" File Watcher stopped safely by user.")
    
    observer.join()

if __name__ == "__main__":
    start_file_watcher()


# 21 Optimize memory While loading large CSVs

def load_csv_optimized(file_path :str, usecols:list=None , dtype_mapping:dict=None , chunksize:int = None):
    """Loads  a large CSV file with extreme memory optimization by filtering columns 
    downcasting datatypes or processing in chunks"""

    if not os.path.exists(file_path):

        raise FileNotFoundError(f"CSV file not found:{file_path}")


    try:
        logger.info(f"Optimize loading started for :{file_path}")

        # If you can give the chunksize the create the generator return
        if chunksize:
            logger.info(f"Loading CSV in memory-efficient chunks of {chunksize:,}rows..")
            return pd.read_csv(
                file_path,
                usecols=usecols,
                dtype=dtype_mapping,
                chunksize=chunksize,
                low_memory=True
            )
        # Normal optimized load
        df=pd.read_csv(
            file_path,
            usecols=usecols,
            dtype=dtype_mapping,
            low_memory=True
        )
        mem_usage=df.memory_usage(deep=True).sum()/(1024 * 1024)
        logger.info(f"Successfullly loaded CSV cleanly .Shape :{df.shape}RAM Usage:{mem_usage:.2f}MB")

        return df
    except Exception as e:
        logger.error(f"Error in optimized CSV loafing :{e}")
        raise

#Part D Data cleanign & Missing value management
def handle_missing_values(df:pd.DataFrame,strategy:str ='auto' , fill_values:dict =None)->pd.date_range:
    """Intelligently handles missing values in a pandas dataframe base on data types 
    and automated imputation strategies (mediam for numbers "Unknown for categories)
    """
    if  df is None or df.empty:
        logger.warning("DataFrame is None and empty , Missing value treatment will skip")
        return df

    try:
        logger.info("Starting intelligent missing value impitation ..")
        initial_missing=df.isnull().sum().sum()
        logger.info(f"Total missing value found across dataset :{initial_missing:,}")

        if initial_missing == 0:
            logger.info("DataFram is not have any missing value ! DataFrame is clean ")
            return df
        df_clean =df.copy()

        # Make numerical and categorical columns acre different
        num_col=df_clean.select_dtypes(include=['number']).columns
        cat_cols=df_clean.select_dtypes(include=['object','category']).columns

        # if user can give the custome dictionary then we will fill it first
        if fill_values and isinstance(fill_values,dict):
            for col,val in fill_values.itemS():
                if col in df_clean.columns:
                    df_clean[col]=df_clean.fillna(val)
                    logger.info(f"fill the coulmn with the custome value {col}:{val}")
        #Intelligent Automated Imputation Strategy

        if strategy =='auto':
            #Numerical columns:fill with the median(to protect with the outliers)
            for col in num_col:
                if df_clean[col].isnull().any():
                    fill_val=df_clean[col].median()
                    df_clean[col]=df_clean[col].fillna(fill_val)
                    logger.info(f"Numerical column '{col}' fill with median {fill_val}")

            #  Categorical columns :fill with the unknows  thats why category will don't lose

            for col in cat_cols:
                if df_clean[col].isnull().any():
                    fill_val='Unknown'
                    df_clean[col]=df_clean[col].fillna(fill_val) 
                    logger.info(f"Categorical column {col} to fill with the default value :{fill_val}")

        elif strategy =="drop":
            before_len =len(df_clean) 
            df_clean=df_clean.dropna()
            logger.info(f"Row with missing value dropped Total rows removed :{before_len -len(df_clean):,}")

        remaining_missing = df_clean.isnull().sum().sum()
        logger.info(f"Missing Value treatment successfully complete .Remaining missing values {remaining_missing}")

        return df_clean
    except Exception as e:
        logger.error(f"Error handling missing values {e}")
        raise


# part D 23 Outliersdetection and removal utility

def detect_and_remove_outliers(df:pd.DataFrame,columns: list=None,threshold:float =1.5)->pd.DataFrame:
    """detects and removes outliers from numrical columns in a pandas datafram
    using the IQR (Interquartile range) method
    """
    
    
    if df is None or df.empty:
        logger.warning ("Dataframe is empty and None that's why outlier is skip")
        return df
    if len(df) < 10:
            logger.warning("DataFrame mein rows bohot kam hain (< 10). IQR outlier detection reliable nahi hai, skipping...")
            return df

    df_clean = df.copy()
    initial_rows=len(df_clean)

    # If this one is not provide specific column then select the  numerical columns

    if columns is None:
        columns=df_clean.select_dtypes(include=['number']).columns.tolist()
    try:
        logger.info(f"Starting outlier detection using IQR method on columns: {columns}")

        for col in columns:
            if col in df_clean.columns:
                # Calculate Q1 is (25th percentile) and Q3(75th percentile)
                Q1 = df_clean[col].quantile(0.25)
                Q3 = df_clean [col].quantile(0.75)
                IQR =Q3-Q1

                lower_bound =Q1 -(threshold *IQR)
                upper_bound =Q3 -(threshold *IQR)

                before_count =len(df_clean)

                #filter out rows outside the bounds

                df_clean =df_clean[(df_clean[col]>= lower_bound)&(df_clean[col]<=upper_bound)]
                removed = before_count-len(df_clean)

                if removed >0:
                    logger.info(f"-> Column {col}:Removed {removed} outliers (Bounds:[{lower_bound:.2f},{upper_bound:.2f}])")
        total_removed = initial_rows-len(df_clean)
        logger.info(f"Outlier removel complete Total rows removed :{total_removed}|Remaining rows:{len(df_clean):,}")

        return df_clean
    except Exception as e:
        logger.error(f"Error during outlier detection and removal :{e}")
        raise


#Part D 24 Duplicate Records Removel Utility

def remove_duplicate_records(df:pd.DataFrame, subset_cols:list=None, keep_strateg:str='first')->pd.DataFrame:
    """
    Detects and removes duplicate rows from a pandas Dataframe 
    can check across all columns or specific subset columns
    """
    if df is None or df.empty:
        logger.warning("DataFrame is empty and None that's why Duplicate remove skip ")
        return df

    try:
        initial_rows=len(df)
        logger.info(f"Starting duplicate records check . Initial row count:{initial_rows:,}")

        #Drop duplicate based on subset columns or entire row

        df_clean=df.drop_duplicates(subset=subset_cols, keep=keep_strateg)

        removed_rows=initial_rows-len(df_clean)

        if removed_rows >0:
            logger.info(f"Successfully removed {removed_rows} duplicate records .removed row :{len(df_clean)}")

        else:
            logger.info("dataframe means nathing duplicate records :dataframe is empty ")

        return df_clean
    except Exception as e:
        logger.error(f"Error Removeing duplicate records :{e}")
        raise


#Part D Multi Dataframe marger & concatenation

pyflow_marge_dfs_doc="Marges or concatenates multiple pandas dataframe efficiently"

def marge_dataframes(df_list:list , how : str="inner", on: str =None, axis :int =0)->pd.DataFrame:
    """Combines multiple dataframe either vertically (concatenetion) or horizontally (merging)
    based on specified strategies and key """

    if not df_list or not isinstance(df_list, list):
        logger.warning("Don't have the valid dataframe . that's why we skip the merge operation")
        return pd.DataFrame()


    try:
        # if the axis is 0 then create vertical concatenate (one by one)
        if axis ==0:
            logger.info(f"Vetically concatenationg {len(df_list) }dataframe")
            merged_df =pd.concat(df_list,ignore_index=True)

            logger.info(f"Concatenation successful .final shape:{merged_df.shape}")
            return merged_df

        #If axis is 1 then create marging 
        elif axis==1 and len(df_list)>=2:
            logger.info(f"Horizontally mergin Dataframe using '{how}' join on key '{on}")
            merged_df=df_list[0]
            for i,next_df in enumerate(df_list[1:],start=1):
                merged_df=pd.merge(merged_df,next_df,how=how, on=on)

            logger.info(f"Merge successful fine shape :{merged_df.shape}")
            return merged_df
        else:
            logger.warning("Invalid merge arguments provided Returing first dataframe ")
            return df_list[0]

    except Exception as e:
        logger.error(f"Error during DataFrame merging/Concatenation :{e}")
        raise


# part D q 26

def perform_advanced_aggregation(df:pd.DataFrame,group_by_cols:list,agg_dict:dict)->pd.DataFrame:
    """Perform avdanced group by aggregation on a pandas dataframe using multiple
    custome fucntion (sum,mean ,count,,min,max) across specifid columns"""

    if df is None or df.empty:
        logger.warning("dataframe is empty and none that why skip the aggregation..")
        return pd.DataFrame()

    try:
        logger.info(f"Starting advanced aggregation grouped by : {group_by_cols}with metrics :{agg_dict}")

        agg_df=df.groupby(group_by_cols).agg(agg_dict).reset_index()

        logger.info(f"Aggeration successful.Resulting shape {agg_df.shape}")
        return agg_df

    except Exception as e:
        logger.error(f"Error during advanced aggregation {e}")
        raise




# Part D question 27  date and time transformation utility

def transform_datetime_columns(df:pd.DataFrame,date_cols:list,extract_features: bool=True)->pd.DataFrame:
    """Converts specified columns to pandas datetime format and optinally extracts
    useful temporal features (year , month, day ,dayofweek ,hours)"""

    if df is None or df.empty:
        logger.warning("Dataframe is empty or None that's why date Transformation is skip")
        return df

    if not date_cols:
        logger.warning("No any date column is specify ")
        return df
    df_clean = df.copy()
    try:
        logger.info(f"Starting datetime transformation on columns {date_cols}")

        for col in date_cols:
            if col in df_clean.columns:
                # convert to datetime safely (Invalid parses become not)

                df_clean[col]=pd.to_datetime(df_clean[col],errors='coerce')
                logger.info(f"Successfully converted column {col} to datetime")

                # Extract temporal features if requested

                if extract_features:
                    df_clean[f'{col}_year'] = df_clean[col].dt.year
                    df_clean[f'{col}_month'] = df_clean[col].dt.month
                    df_clean[f'{col}_day'] = df_clean[col].dt.day
                    df_clean[f'{col}_dayofweek'] = df_clean[col].dt.day_name()
                    df_clean[f'{col}_hour'] = df_clean[col].dt.hour
                    logger.info(f"Extracted temporal features for '{col}': year, month, day, dayofweek, hour.")

        return df_clean

    except Exception as e:
        logger.error(f"Error during datetime transformation: {e}")
        raise

# Question 28 Rolling  window analytics

def calculate_rolling_metrics(df:pd.dataframe, value_cols: list,window:int=3,agg_funcs:list=['mean','sum'])->pd.dataframe:
    """Calculates rolling window metics(rolling mean, rolling sum)
    on specified numberical columns using a pandas rolling window"""

    if df is None or df.empty:
        logger.warning("Dataframe is emoty or None that's why we skip rolling window analysis ")
        return df
    if not value_cols:
        logger.warning("No any value columns is specify for the rolling analytics ")
        return df

    df_clean = df.copy()

    try:
        logger.info(f"Starting rolling window analytics (window size={window} on columns{value_cols})")


        for col in value_cols:
            if col in df_clean.columns:
                for func in agg_funcs:
                    new_col_name=f"{col}_rolling_{window}-{func}"

                    if func =="mean":
                        df_clean[new_col_name]=df_clean[col].rolling(window=window).mean()
                    elif func =="sum":
                        df_clean[new_col_name]=df_clean[col].rolling(window=window).sum()
                    elif func =="min":
                        df_clean[new_col_name]=df_clean[col].rolling(window=window).min()
                    elif func =="max":
                        df_clean[new_col_name]=df_clean[col].rolling(window=window).max()
                    elif func =="std":
                        df_clean[new_col_name]=df_clean[col].rolling(window=window).std()

                logger.info(f"Calculated rolling metrics ({agg_funcs}) for '{col}' with window size {window}.")

        return df_clean

    except Exception as e:
        logger.error(f"Error during rolling window analytics: {e}")
        raise


def filter_dataframe_by_query(df:pd.dataframe,query_string:str)->pd.DataFrame:
    """Filter a pandas Dataframe using an SQL like query string expression"""

    if df is None or df.empty:
        logger.warning("Dataframe is empty and None That's why query filter is skip")
        return df

    if not query_string or not isinstance(query_string,str):
        logger.warning("Valid query string is not provided ")
        return df

    try:
        logger.info(f"Applying query base filtering with expression {query_string}")
        initial_rows =len(df)

        # use the pandas query method for the filter

        filtered_df = df.query(query_string).copy()

        remaining_rows =len(filtered_df)
        removed_rows =initial_rows-remaining_rows
        logger.info(f"Query filtering successful.rows before {initial_rows:,}Rows after {remaining_rows} (filtered out:{removed_rows})")

        return filtered_df
    except Exception as e:
        logger.error(f"Error during query-based filtering with exprecssion {query_string},{e}")
        raise


from pathlib import Path

def export_dataframe_formats(
        df:pd.DataFrame,
        base_output_path:str,
        formats: list =None,
        index :bool = False
)->dict:

    """Exports a pandas dataframe to one or more file formate (csv,parquet,json,excel)
Returns a dictionary mapping each format to its saved file path"""

    if df is None or df.empty:
        logger.warning("DataFrame is empty and none that's why we skip the export")
        return{}

    if not formats:
        format =["CSV","parquet"]

    base_path = Path(base_output_path)
    base_path.parent.mkdir(parents=True ,exist_ok=True)

    exported_files={}

    try: 
        logger.info (f"Starting export for {base_path} in formats:{formats}")

        for fmt in formats:
            fmt_clean = fmt.lower().strip()
            target_file = base_path.with_suffix(f".{fmt_clean}" if fmt_clean != 'Excel'else '.xlsx')

            if fmt_clean =="csv":
                df.to_csv(target_file,index=index)
            elif fmt_clean =="parquet":
                df.to_parquet(target_file,index=index)
            elif fmt_clean == 'json':
                df.to_json(target_file,orient='records',index=2,date_format='iso')
            elif fmt_clean in ("excel","xlsx"): 
                df.to_excel(target_file,index=index)
            else:
                logger.warning(f"Unsupported export format {fmt},skipping")
                continue

            exported_files[fmt] =str(target_file)
            logger.info(f"Exported {fmt_clean}, successfull ->{target_file}")

        return exported_files
    except Exception as e:
        logger.error(f"Error during exporting dataframe to {formats}: {e}")
        raise