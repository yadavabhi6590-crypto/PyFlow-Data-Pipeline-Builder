from pyflow.utils import deduplicate_trips_with_class # ya jahan bhi rakhega

if __name__ == "__main__":
    print("--- TripRecord OOP Deduplication Test ---")
    parquet_path = "data/yellow_tripdata_2024-01.parquet"
    
    try:
        stats = deduplicate_trips_with_class(parquet_path, sample_limit=10000)
        print("\n[SUCCESS] Deduplication Completed:")
        print(f" -> Total Rows Processed : {stats['total_processed']:,}")
        print(f" -> Unique TripRecords   : {stats['unique_records']:,}")
        print(f" -> Duplicates Removed   : {stats['duplicates_found']:,}")
    except Exception as e:
        print(f"[ERROR] {e}")