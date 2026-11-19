from pyflow.utils import process_csv_with_auto_encoding

if __name__ == "__main__":
    print("--- Automatic File Encoding Detection Test ---")
    
    csv_path = "data/gdp.csv"  # ya koi bhi CSV file
    
    try:
        stats = process_csv_with_auto_encoding(csv_path, chunk_size=50000)
        
        print("\n[SUCCESS] Encoding Detection & Processing Completed:")
        print(f" -> Detected Encoding : {stats['detected_encoding']}")
        print(f" -> Confidence Score  : {stats['confidence'] * 100}%")
        print(f" -> Total Chunks      : {stats['total_chunks']}")
        print(f" -> Total Rows Read   : {stats['total_rows']:,}")
        
    except Exception as e:
        print(f"[ERROR] {e}")