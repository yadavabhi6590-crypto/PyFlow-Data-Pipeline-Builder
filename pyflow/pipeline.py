from pathlib import Path
import time
from pyflow.config import ConfigManager
from pyflow.extractors import DataExtractor
from pyflow.transformeres import dataTransformer
from pyflow.loaders import Dataloader
from pyflow.utils import logger


class PyflowPipeline:
    def __init__(self,config_path:str="config/pipeline.yaml"):
        self.config_path =Path(config_path)
        self.config_manager =None

    def run(self)->dict:
        start_time = time.perf_counter()
        logger.info(f"+++ Pyflow pipeline started | config :{self.config_path}+++")

        try:
            logger.info("[Step 1/4]Loading configuration")
            self.config_manager=ConfigManager(str(self.config_path))
            ext_cfg=self.config_manager.get("extract")
            tr_cfg=self.config_manager.get("transform")
            ld_cfg=self.config_manager.get("load")

            #step 2 raw data extract karna

            logger.info(["Step 2/4 Extracting raw data"])
            extractor=DataExtractor(base_dir=ext_cfg.get("base_dir","data"))
            raw_df=extractor.extract(
                file_name=ext_cfg.get("file_name"),
                file_type=ext_cfg.get("file_type")
            )
            #step 3 

            logger.info("[step3/4]Transdorming data")
            transformer =dataTransformer(raw_df)

            datetime_col=tr_cfg.get("datetime_col")
            if datetime_col:
                transformer.parse_datetime(datetime_col)

            drop_subset= tr_cfg.get("drop_missing_subset")
            if drop_subset:
                transformer.drop_missing(subset=drop_subset)
            if tr_cfg.get("deduplicate",True):
                transformer.remove_duplicates()

            filter_query =tr_cfg.get("filter_query")
            if filter_query:
                transformer.filter_query(filter_query)

            clean_df=transformer.get_df()

            # Step 4: Transformed data load/save karna
            logger.info("[Step 4/4] Loading transformed data")  # Step 4 start ka log
            loader = Dataloader(output_dir=ld_cfg.get("output_dir", "output"))  # Config se output folder liya ('output_dir' lowercase)
            saved_files = loader.load(  # Sahi keys ke sath arguments pass kiye
                df=clean_df,  # Cleaned DataFrame
                file_name=ld_cfg.get("file_name", "cleaned_trips"),  # 'file_name' se output base name (str) liya
                formats=ld_cfg.get("formats", ["csv", "parquet"]),  # 'formats' se list li; quotes aur key naam sahi kiya
                index=ld_cfg.get("index", False),  # Row index column save nahi karna
            )

       
            elapsed=time.perf_counter() -start_time
            logger.info(f"===Pyflow pipeline completed in {elapsed:.2}s===")
            return saved_files
        except Exception as e:
            elapsed = time.perf_counter()-start_time
            logger.error(f"===Pyflow pipeline failed after {elapsed:.2f},{e}===")
            raise
            