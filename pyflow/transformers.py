import pandas as pd
from pyflow.utils import logger

class dataTransformer:
    def __init__(self,df:pd.DataFrame):
        self.df=df.copy() if df is not None else pd.DataFrame()
        logger.info (f"Datatransformer initialized with shape :{self.df.shape}")

    def drop_missing(self, subset: list = None) -> "dataTransformer":  # Missing rows hatata hai aur chaining ke liye 'self' return karta hai
         before = len(self.df)  # Hatane se pehle ki total rows
         if subset is not None:  # Specific columns diye gaye hain toh
            missing_cols = [c for c in subset if c not in self.df.columns]  # Jo column table mein nahi hai use alag nikala
            if missing_cols:  # Missing column mila toh warning log ki
                logger.warning(f"Columns not found for drop_missing, skipping them: {missing_cols}")  # Warning record ki
            valid_subset = [c for c in subset if c in self.df.columns]  # Sirf maujood columns rakhe
            if not valid_subset:  # Koi bhi column match nahi hua toh dropna skip kiya
                return self  # Method chaining ke liye 'self' return kiya
            self.df = self.df.dropna(subset=valid_subset)  # Valid columns par null rows hatayin
         else:  # subset None ho toh poore DataFrame se null rows hatayega
            self.df = self.df.dropna()  # Sabhi columns check karke null rows hatayin
         logger.info(f"Dropped missing rows: {before - len(self.df):,} removed, {len(self.df):,} remaining")  # Result log kiya
         return self  # Method chaining ke liye 'self' return kiya
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

    def filter_query(self, query: str):  # Filter method ke andar check karne ke liye
    #   breakpoint()  # Python 3.7+ mein yahan code ruk jayega aur (Pdb) prompt khulega
      self.df = self.df.query(query)
      return self