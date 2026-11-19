from pathlib import Path
import pandas as pd
from pyflow.utils import logger



class Dataloader:
    def __init__(self,output_dir:str='output'):
        self.output_dir =Path(output_dir)
        self.output_dir.mkdir(parents=True ,exist_ok=True)
        logger.info(f"dataloader initialized with otuput_dir :{self.output_dir}")


    def load (self,df:pd.DataFrame ,file_name :str,formats:list =None, index:bool=False) ->dict:
        if df is None or df.empty:
            logger.warning("Dataframe is empty or None :Skipping load")
            return{}

        if not formats:
            formats =['csv','parquet']

        base_path =self.output_dir/Path(file_name).stem
        saved_file ={}

        for fmt in formats:
            fmt_clean =str(fmt).lower().strip()
            ext=".xlsx" if fmt_clean in ('excel','xlsx')else f".{fmt_clean}"
            target_file =base_path.with_suffix(ext)

            try:
                if fmt_clean =="csv":
                    df.to_csv(target_file,index=index)
                elif fmt_clean =="parquet":
                    df.to_csv(target_file,index=index)
                elif fmt_clean =="json":
                    df.to_parquet(target_file,index=index,engine='pyarrow')
                elif fmt_clean in('excel','xlsx'):
                    df.to_excel(target_file,index=index)
                else:
                    logger.warning(f"Unsupported format {fmt} skipping")
                    continue
                saved_file[fmt_clean]=str(target_file)
                logger.info(f"Loaded {fmt_clean} successfully ->{target_file}")

            except Exception as e:
                logger.error(f"Failed loadig {fmt_clean} to {target_file}:{e}")
                raise 
        return saved_file