

from pathlib import Path
import time
from tqdm import tqdm

from pyflow.config import ConfigManager
from pyflow.extractors import DataExtractor
from pyflow.transformers import dataTransformer
from pyflow.loaders import Dataloader
from pyflow.profiler import DataProfiler
from pyflow.utils import logger, retry_with_backoff
from pyflow.validators import DataValidator


class PyflowPipeline:
    def __init__(self, config_path: str = "config/pipeline.yaml"):
        self.config_path = Path(config_path)
        self.config_manager = None

    @retry_with_backoff(max_retries=3, base_delay=1.0, backoff_factor=2.0)
    def _extract_with_retry(self, extractor: DataExtractor, ext_cfg: dict):
        return extractor.extract(
            file_name=ext_cfg.get("file_name"),
            file_type=ext_cfg.get("file_type"),
        )

    @retry_with_backoff(max_retries=3, base_delay=1.0, backoff_factor=2.0)
    def _load_with_retry(self, loader: Dataloader, clean_df, ld_cfg: dict):
        return loader.load(
            df=clean_df,
            file_name=ld_cfg.get("file_name", "cleaned_trips"),
            formats=ld_cfg.get("formats", ["csv", "parquet"]),
            index=ld_cfg.get("index", False),
        )

    def run(self, dry_run: bool = False) -> dict:
        start_time = time.perf_counter()
        logger.info(f"+++ Pyflow pipeline started | config : {self.config_path} +++")

        with tqdm(total=5, desc="Pyflow ETL", unit="stage") as pbar:
            try:
                pbar.set_postfix_str("Config")
                logger.info("[Step 1/5] Loading configuration")
                self.config_manager = ConfigManager(str(self.config_path))
                ext_cfg = self.config_manager.get("extract") or {}
                tr_cfg = self.config_manager.get("transform") or {}
                val_cfg = self.config_manager.get("validate") or {}
                ld_cfg = self.config_manager.get("load") or {}
                pbar.update(1)

                pbar.set_postfix_str("Extract")
                logger.info("[Step 2/5] Extracting raw data")
                extractor = DataExtractor(base_dir=ext_cfg.get("base_dir", "data"))
                raw_df = self._extract_with_retry(extractor, ext_cfg)
                pbar.update(1)

                pbar.set_postfix_str("Transform")
                logger.info("[Step 3/5] Transforming data")
                transformer = dataTransformer(raw_df)

                datetime_col = tr_cfg.get("datetime_col")
                if datetime_col:
                    transformer.parse_datetime(datetime_col)

                drop_subset = tr_cfg.get("drop_missing_subset")
                if drop_subset:
                    transformer.drop_missing(subset=drop_subset)

                if tr_cfg.get("deduplicate", True):
                    transformer.remove_duplicates()

                filter_query = tr_cfg.get("filter_query")
                if filter_query:
                    transformer.filter_query(filter_query)

                clean_df = transformer.get_df()
                pbar.update(1)

                pbar.set_postfix_str("Validate & Profile")
                logger.info("[Step 4/5] Validating transformed data")
                validator = DataValidator(
                    required_columns=val_cfg.get("required_columns", []),
                    positive_columns=val_cfg.get("positive_columns", []),
                )
                clean_df = validator.validate(clean_df)

                prof_cfg = self.config_manager.get("profile") or {}
                if prof_cfg.get("enabled", True):
                    profiler = DataProfiler(output_dir=prof_cfg.get("output_dir", "reports"))
                    profiler.generate(clean_df, name=prof_cfg.get("report_name", "cleaned_trips_profile"))
                pbar.update(1)

                if dry_run:
                    pbar.set_postfix_str("Dry-run done")
                    elapsed = time.perf_counter() - start_time
                    logger.info(f"=== Pyflow dry-run completed in {elapsed:.2f}s (no files written) ===")
                    return {}

                pbar.set_postfix_str("Load")
                logger.info("[Step 5/5] Loading transformed data")
                loader = Dataloader(output_dir=ld_cfg.get("output_dir", "output"))
                saved_files = self._load_with_retry(loader, clean_df, ld_cfg)
                pbar.update(1)

                elapsed = time.perf_counter() - start_time
                logger.info(f"=== Pyflow pipeline completed in {elapsed:.2f}s ===")
                return saved_files

            except Exception as e:
                elapsed = time.perf_counter() - start_time
                logger.error(f"=== Pyflow pipeline failed after {elapsed:.2f}s: {e} ===")
                raise