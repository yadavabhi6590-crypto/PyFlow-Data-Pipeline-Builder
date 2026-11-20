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

        if not formats:  # Formats list khali ya None ho toh default formats set karega
            formats = ["csv", "parquet"]  # Default output formats

        if isinstance(file_name, (list, tuple)):  # Defensive check: galti se list aaye toh crash na ho
            logger.warning(f"Expected string for file_name, got {type(file_name).__name__}; using fallback.")  # Warning log ki
            file_name = str(file_name[0]) if file_name else "cleaned_trips"  # Safe string fallback liya

        base_path = self.output_dir / Path(str(file_name)).stem  # Output directory + clean file stem (bina extension ke)
        saved_file = {}  # Save hui files ka record rakhne ke liye dict

        for fmt in formats:  # Har requested format ke liye loop chalega
            fmt_clean = str(fmt).lower().strip()  # Format naam ko lowercase aur space-free banaya
            ext = ".xlsx" if fmt_clean in ("excel", "xlsx") else f".{fmt_clean}"  # Excel ke liye .xlsx, baaki ke liye .fmt
            target_file = base_path.with_suffix(ext)  # Final target file path banaya

            try:  # File write karte waqt koi error aaye toh handle karne ke liye
                if fmt_clean == "csv":  # CSV format ke liye
                    df.to_csv(target_file, index=index)  # CSV file likhi
                elif fmt_clean == "parquet":  # Parquet format ke liye
                    df.to_parquet(target_file, index=index, engine="pyarrow")  # Asli Parquet file likhi (to_csv nahi)
                elif fmt_clean == "json":  # JSON format ke liye
                    df.to_json(target_file, orient="records", indent=2)  # Asli JSON file likhi (to_parquet nahi)
                elif fmt_clean in ("excel", "xlsx"):  # Excel format ke liye
                    df.to_excel(target_file, index=index)  # Excel file likhi
                else:  # Unsupported format aaye toh
                    logger.warning(f"Unsupported format {fmt} skipping")  # Warning log karke skip kiya
                    continue  # Agle format par jao

                saved_file[fmt_clean] = str(target_file)  # Successful file path dict mein save kiya
                logger.info(f"Loaded {fmt_clean} successfully -> {target_file}")  # Success log likha

            except Exception as e:  # Koi write error aaye toh
                logger.error(f"Failed loading {fmt_clean} to {target_file}: {e}")  # Error log kiya
                raise  # Error caller ko bheja

        return saved_file  # Sabhi saved file paths ki dictionary return ki