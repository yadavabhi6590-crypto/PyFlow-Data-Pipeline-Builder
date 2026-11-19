from pyflow.utils import analyze_pickup_locations

if __name__ =="__main__":
    print("__Part B Question 1 Counter for Pickup location Frequency")

    # put your taxi file path from there 
    taxi_csv_path = "D:\\tutedude\\Python_Project_t\\PyFlow_Assignment_2\\data\\yellow_tripdata_2024-01.parquet"
    try:
        top_pickups=analyze_pickup_locations(taxi_csv_path,top_n=5)


        print("[Success] Top busiest Pickup location Ids")
        for loc_id, count in top_pickups.items():
            print(f"Locations ID {loc_id}: {count} Pickups")

    except Exception as e:
        print(f"[Error] Test fail ho gaya: {e}")