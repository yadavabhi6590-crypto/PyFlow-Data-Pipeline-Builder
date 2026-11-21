from pyflow.utils import analyze_hourly_fares_parquet

if __name__ == "__main__":
    print("--- Part B - Question 2: Hourly Fare Analysis Test ---")
    
    parquet_path = "D:\\tutedude\\Python_Project_t\\PyFlow_Assignment_2\\data\\yellow_tripdata_2024-01.parquet"
    
    try:
        hourly_avg = analyze_hourly_fares_parquet(parquet_path)
        
        print("\n[SUCCESS] Average Taxi Fare by Hour of the Day (0-23):")
        for hour, avg_fare in hourly_avg.items():
            print(f" -> Hour {hour:02d}:00 -> Average Fare: ${avg_fare}")
            
    except Exception as e:
        print(f"[ERROR] Test fail ho gaya: {e}")