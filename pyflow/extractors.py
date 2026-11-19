
from pathlib import Path
import pandas as pd
from pyflow.utils import logger


class DataExtractor:

    """Read all files from dist into a pandas dataframe"""

    def __init__(self,base_dir:str ='data'):
        self.base_dir=Path(base_dir)
        logger.info(f"DataExtractor ready with base_dir :{self.base_dir}")

    def extract(self,file_name:str,file_type:str=None) ->pd.DataFrame:
        file_path=self.base_dir/file_name

        if not file_path.exists():
            msg=f"Filenot found.{file_path}"
            logger.error(msg) 
            raise FileNotFoundError(msg)

        fmt=(file_type or file_path.suffix.lstrip(".")).lower().strip()
        logger.info(f"Extracting {file_path} as (fmt)") 

        try:
            if fmt=="csv":
                df=pd.read_csv(file_path)
            elif fmt =="parquet":
                df=pd.read_parquet(file_path ,engine="pyarrow")
            elif fmt=="json": 
                df=pd.read_jsom(file_path)
            elif fmt in("excel","xlsx","xls"):
                df=pd.read_excel(file_path)
            else:
                msg=f"Unsupported file format:{fmt}"
                raise ValueError(msg)

            logger.info(f"Loaded {len(df):,}rows,{len(df.columns)} cols from {file_path}")
            return df
        except Exception as e: 
            logger.error (f"Extraction failed for {file_path},:{e}")
            raise