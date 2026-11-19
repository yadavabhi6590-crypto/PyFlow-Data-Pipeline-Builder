

from pyflow.utils import process_CSV_with_error_handling



if __name__=="__main__":
    print("__Corruoted CSV handling test__")

    csv_path ="D:\\tutedude\\Python_Project_t\\PyFlow_Assignment_2\\data\\us-counties-2023.csv"

    try:
        stats=process_CSV_with_error_handling(csv_path,chunk_size=50000)

        print("\n[SUCCESS] Robust CSV Processing completed:")
        print(f"->Status    :{stats['status']}")
        print(f"-> Total chunks   :{stats['total_chunks']}")
        print(f"-> Valid Rows read :{stats['Valid_rows_processed']}")

    except Exception as e:
        print(f"[ERROR]{e}")