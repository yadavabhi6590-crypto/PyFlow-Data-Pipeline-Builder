

from pyflow.utils import process_large_csv_in_chunks

if __name__=="__main__":
    print("__Large CSV chunk processing Test ----")

    csv_path="D:\\tutedude\\Python_Project_t\\PyFlow_Assignment_2\\data\\gdp.csv"

    try:
        stats=process_large_csv_in_chunks(csv_path,chunk_size=50000)
       
        print("\n[SUCCESS] Chunk Processing Completed:")
        print(f" -> Chunks Processed : {stats['total_chunks_processed']}")
        print(f" -> Total Rows Read  : {stats['total_rows']:,}")
        print(f" -> Overall Avg Fare : ${stats['average_fare']}")
        print(f" -> Max Fare Found   : ${stats['max_fare']}")
        print(f" -> Min Fare Found   : ${stats['min_fare']}")
        
    except Exception as e:
        print(f"[ERROR] {e}")


