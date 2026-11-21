


from pyflow.config import ConfigManager
from pyflow.extractors import DataExtractor
from pyflow.transformers import dataTransformer
from pyflow.loaders import Dataloader

if __name__ =="__main__":
    cfg=ConfigManager("config/pipeline.yaml")

    ext_cfg=cfg.get("extract")
    tr_cfg=cfg.get("transform")
    ld_cfg=cfg.get("load")

    extractor = DataExtractor(base_dir=ext_cfg.get("base_dir", "data"))  # Config se input folder liya
    raw_df = extractor.extract(  # Config se file_name aur file_type le kar data load kiya
        file_name=ext_cfg.get("file_name"),
        file_type=ext_cfg.get("file_type"),
    )

    transformer = dataTransformer(raw_df)  # Raw DataFrame transformer ko diya
    if tr_cfg.get("datetime_col"):  # Config mein datetime_col ho toh parse karega
        transformer.parse_datetime(tr_cfg["datetime_col"])  # Date column parse kiya
    if tr_cfg.get("drop_missing_subset"):  # Config mein subset ho toh missing rows hatayega
        transformer.drop_missing(subset=tr_cfg["drop_missing_subset"])  # Missing rows hatayin
    if tr_cfg.get("deduplicate", True):  # Config ke hisaab se duplicates hatayega
        transformer.remove_duplicates()  # Duplicate rows hatayin
    if tr_cfg.get("filter_query"):  # Config mein filter_query ho toh rows filter karega
        transformer.filter_query(tr_cfg["filter_query"])  # Query apply ki
    clean_df = transformer.get_df()  # Final clean DataFrame liya

    loader = Dataloader(output_dir=ld_cfg.get("output_dir", "output"))  # Config se output folder liya
    saved = loader.load(  # Config ke file_name, formats aur index se files save kin
        df=clean_df,
        file_name=ld_cfg.get("file_name", "output_data"),
        formats=ld_cfg.get("formats", ["csv", "parquet"]),
        index=ld_cfg.get("index", False),
    )

    print("Pipeline saved files:", saved)