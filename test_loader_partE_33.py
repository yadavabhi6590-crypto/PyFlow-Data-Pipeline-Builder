

from pyflow.extractors import DataExtractor  # extractors.py se DataExtractor laaya
from pyflow.transformeres import dataTransformer  # transformeres.py se DataTransformer laaya
from pyflow.loaders import Dataloader  # loader.py se DataLoader laaya

if __name__ == "__main__":  # Sirf direct run hone par chalega
    extractor = DataExtractor(base_dir="data")  # 'data' folder se read karne ke liye extractor banaya
    raw_df = extractor.extract("us-counties-2023.csv")  # Raw CSV load kiya

    clean_df = (  # Method chaining se data clean aur filter kiya
        dataTransformer(raw_df)  # Raw DataFrame transformer ko diya
        .parse_datetime("date")  # 'date' column ko datetime mein badla
        .drop_missing(subset=["date", "cases"])  # Missing date/cases wali rows hatayin
        .remove_duplicates()  # Duplicate rows hatayin
        .filter_query("state == 'Texas' and cases > 50000")  # Texas ke cases > 50000 records filter kiye
        .get_df()  # Final DataFrame nikala
    )

    loader = Dataloader(output_dir="output")  # 'output' folder ke sath loader banaya
    files = loader.load(clean_df, "texas_high_cases", formats=["csv", "parquet", "json"])  # Clean data ko 3 formats mein save kiya
    print("Saved files:", files)  # Saved file paths print kiye