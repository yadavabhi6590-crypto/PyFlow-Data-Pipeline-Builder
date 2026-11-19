from pyflow.utils import calculate_rolling_fare_average

if __name__ == "__main__":
    print("--- Part B - Question 3: Deque Rolling Buffer Test ---")
    
    parquet_path = "data/yellow_tripdata_2024-01.parquet"
    
    try:
        # Window size 100 rakhte hain (matlab pichli 100 rides ka moving average)
        latest_averages = calculate_rolling_fare_average(parquet_path, window_size=100)
        
        print("\n[SUCCESS] Latest 10 Rolling Moving Averages (Window Size = 100):")
        for idx, avg in enumerate(latest_averages, start=1):
            print(f" -> Buffer Snapshot {idx}: Moving Avg Fare = ${avg}")
            
    except Exception as e:
        print(f"[ERROR] Test fail ho gaya: {e}")