


from pathlib import Path
import pandas as pd
from pyflow.utils import export_dataframe_formats

if __name__ == "__main__":
    print("--- Multi-Format Export Test ---")

    sample_file = Path("D:\\tutedude\\Python_Project_t\\PyFlow_Assignment_2\\data\\us-counties-2023.csv")
    if sample_file.exists():
        df = pd.read_csv(sample_file)
        print(f"Loaded data from {sample_file} with shape {df.shape}")
    else:
        df = pd.DataFrame({
            "id": [1, 2, 3],
            "category": ["A", "B", "A"],
            "amount": [120.5, 340.0, 210.25],
        })
        print("Using fallback sample DataFrame (data/sample.csv not found).")

    # Output files ko 'output/' folder mein save karte hain taaki 'data/' clean rahe
    result = export_dataframe_formats(
        df=df,
        base_output_path="output/exported_data",
        formats=["csv", "parquet", "json"],
        index=False,
    )

    print("\nExported files:")
    for fmt, path in result.items():
        print(f"  {fmt}: {path}")