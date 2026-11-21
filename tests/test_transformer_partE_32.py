


from pyflow.extractors import DataExtractor  # extractors.py se DataExtractor laaya
from pyflow.transformers import dataTransformer  # transformer.py se DataTransformer laaya

if __name__ == "__main__":  # Sirf direct run hone par chalega
    extractor = DataExtractor(base_dir="data")  # 'data' folder ke sath extractor banaya
    raw_df = extractor.extract("us-counties-2023.csv")  # Raw CSV data load kiya

    clean_df = (  # Method chaining se ek ke baad ek transformation chalaya
        dataTransformer(raw_df)  # Raw DataFrame ko transformer mein diya
        .parse_datetime("date")  # 'date' column ko datetime banaya
        .drop_missing(subset=["date", "cases"])  # 'date' ya 'cases' missing ho toh row hatayi
        .remove_duplicates()  # Exact duplicate rows hatayin
        .filter_query("state == 'Texas' and cases > 50000")  # Texas ke un records ko filter kiya jahan cases > 50000 hain
        .get_df()  # Final filtered DataFrame nikala
    )

    print("Transformed shape:", clean_df.shape)  # Filter ke baad bachi rows aur columns
    print(clean_df.head(3))  # Pehli 3 rows check karne ke liye