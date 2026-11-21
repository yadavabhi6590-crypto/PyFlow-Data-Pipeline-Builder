from pyflow.utils import benchmark_list_vs_set_lookup

if __name__ == "__main__":
    print("--- Part B - Question 4: List vs Set Lookup Performance Test ---")
    
    parquet_path = "data/yellow_tripdata_2024-01.parquet"
    
    try:
        results = benchmark_list_vs_set_lookup(parquet_path, sample_size=1000)
        
        print("\n[SUCCESS] Performance Benchmark Results:")
        print(f" -> Total Records in Dataset: {results['total_records']:,}")
        print(f" -> Lookups Performed: {results['sample_lookups']} items")
        print(f" -> Python List Lookup Time : {results['list_time_sec']} seconds")
        print(f" -> Python Set Lookup Time  : {results['set_time_sec']} seconds")
        print(f" -> Speedup Factor          : Set is {results['speedup_factor']}x faster than List!")
        
    except Exception as e:
        print(f"[ERROR] Test fail ho gaya: {e}")