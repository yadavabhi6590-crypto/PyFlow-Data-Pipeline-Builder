import pandas as pd
from pyflow.utils import logger

class dataTransformer:
    def __init__(self,df:pd.DataFrame):
        self.df=df.copy() if df is not None else pd.DataFrame()
        logger.info (f"Datatransformer initialized with shape :{self.df.shape}")

    def drop_missing(self,subset:list=None)->"dataTransformer":
        befor = len (self.df)
        self.df=self.df.dropna(subset=subset)
        logger.info(f"Removedduplicate rows {befor -len(self.df):,}removed ,{len(self.df):,}remaining")
        return self
    def remove_duplicates(self,subset:list=None)->'dataTransformer':
        before= len(self.df)
        self.df=self.df.drop_duplicates(subset=subset)
        logger.info(f"Removed duplicate rows {before -len(self.df):,}removed,{len(self.df):,}remaining")
        return self
    def parse_datetime(self,col:str)->"dataTransformer":
        if col not in self.df.columns:
            logger.warning(f"column {col} not found  in datetime parsing:skiiping")
            return self
        self.df[col]=pd.to_datetime(self.df[col],errors='coerce')
        logger.info(f"Parsed column [col] to datetime")
        return self

    def filter_query(self,query_String:str)->"dataTransformer":
        if not query_String:
            return self 
        before =len(self.df)
        self.df=self.df.query(query_String).copy()

        logger.info(f"Filtered with {query_String},{before}->{len(self.df):,}rows")
        return self

    def get_df(self) -> pd.DataFrame:
        return self.df