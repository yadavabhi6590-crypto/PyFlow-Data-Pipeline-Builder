


import pandas as pd
from pyflow.utils import calculate_rolling_metrics

if __name__ == "__main__":
    print("--- Rolling Window Analytics Test ---")
    
    # Sample sequential data (jaise daily sales)
    data = {
        'day': [1, 2, 3, 4, 5, 6],
        'sales': [100, 150, 200, 250, 300, 350]
    }
    
    df = pd.DataFrame(data)
    print("\nOriginal DataFrame:")
    print(df)
    
    print("\nApplying Rolling Window Analytics (Window Size = 3)...")
    rolling_df = calculate_rolling_metrics(df, value_cols=['sales'], window=3, agg_funcs=['mean', 'sum'])
    
    print("\nResulting DataFrame with Rolling Metrics:")
    print(rolling_df)