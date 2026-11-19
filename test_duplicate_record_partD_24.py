


import pandas as pd
from pyflow.utils import remove_duplicate_records

if __name__ == "__main__":
    print("--- Duplicate Records Removal Test ---")
    
    # Step A: Ek sample DataFrame banate hain jisme kuch rows jaan-booch kar duplicate rakhte hain
    data = {
        'emp_id': [101, 102, 103, 101, 104, 102],          # 101 aur 102 repeat ho rahe hain
        'name': ['Abhishek', 'Rahul', 'Aman', 'Abhishek', 'Priya', 'Rahul'],
        'department': ['IT', 'HR', 'Finance', 'IT', 'Sales', 'HR']
    }
    
    df = pd.DataFrame(data)
    print("\nOriginal DataFrame (with duplicates):")
    print(df)
    print(f"Total initial rows: {len(df)}")
    
    # Step B: Apni PyFlow ki duplicate removal utility call karte hain
    # Yahan hum 'emp_id' ko subset maan rahe hain taaki agar emp_id match ho toh duplicate maan le
    cleaned_df = remove_duplicate_records(df, subset_cols=['emp_id'])
    
    print("\nCleaned DataFrame (after duplicate removal):")
    print(cleaned_df)
    print(f"Total remaining rows: {len(cleaned_df)}")