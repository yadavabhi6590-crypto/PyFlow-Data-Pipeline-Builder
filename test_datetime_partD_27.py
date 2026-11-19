import pandas as pd
from pyflow.utils import transform_datetime_columns

if __name__ == "__main__":
    print("--- Date & Time Transformations Test ---")
    
    # Sample data jisme date string format mein hai
    data = {
        'order_id': [1, 2, 3],
        'order_date': ['2026-05-10 14:30:00', '2026-06-12 09:15:00', '2026-07-20 18:45:00'],
        'amount': [250.5, 450.0, 120.0]
    }
    
    df = pd.DataFrame(data)
    print("\nOriginal DataFrame:")
    print(df)
    
    print("\nApplying Datetime Transformation & Feature Extraction...")
    transformed_df = transform_datetime_columns(df, date_cols=['order_date'], extract_features=True)
    
    print("\nTransformed DataFrame:")
    print(transformed_df.dtypes)
    print(transformed_df)