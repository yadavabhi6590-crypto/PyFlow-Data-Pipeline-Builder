from pyflow.utils import convert_parquet_to_csv

if __name__=="__main__":
    print("---Parquet to CSV Conversion Test---")

    # Path of my input parquet file and target csv output
    parquet_file ="D:\\tutedude\\Python_Project_t\\PyFlow_Assignment_2\\data\\yellow_tripdata_2024-01.parquet"
    csv_output="data/converted_output.csv"

    try:
        result =convert_parquet_to_csv(parquet_file,csv_output)

        print("\n[SUCCESS] Conversion Completed:")
        print(f" -> Status         : {result['status']}")
        print(f" -> Rows Converted : {result['rows_converted']:,}")
        print(f" -> Columns Count  : {result['columns_count']}")
        print(f" -> Saved At       : {result['output_csv']}")
    except Exception as e:
        print(f"[ERROR] {e}")