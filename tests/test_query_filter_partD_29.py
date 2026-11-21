

import pandas as pd
from pyflow.utils import filter_dataframe_by_query

if __name__ == "__main__":
    print("--- Query-Based Filtering Test ---")
    
    # Sample employee dataset
    data = {
        'emp_id': [101, 102, 103, 104, 105],
        'department': ['IT', 'HR', 'IT', 'Finance', 'HR'],
        'salary': [50000, 60000, 75000, 45000, 65000],
        'age': [25, 30, 35, 22, 28]
    }
    
    df = pd.DataFrame(data)
    print("\nOriginal DataFrame:")
    print(df)
    
    # Query Expression: IT department wale ya fir salary 60000 se zyada ho
    query_expr = "department == 'IT' or salary > 60000"
    print(f"\nApplying Query Filter: '{query_expr}'")
    
    filtered_df = filter_dataframe_by_query(df, query_string=query_expr)
    
    print("\nFiltered DataFrame Result:")
    print(filtered_df)