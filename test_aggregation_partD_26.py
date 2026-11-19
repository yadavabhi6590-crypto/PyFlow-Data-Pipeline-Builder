

import pandas as pd
from pyflow.utils import perform_advanced_aggregation

if __name__ == "__main__":
    print("--- Advanced Aggregations Test ---")
    
    # Sample data banate hain employees ka
    data = {
        'department': ['IT', 'HR', 'IT', 'HR', 'Finance', 'Finance'],
        'emp_name': ['Abhishek', 'Rahul', 'Aman', 'Priya', 'Neha', 'Karan'],
        'salary': [50000, 60000, 75000, 55000, 80000, 85000],
        'rating': [4.5, 4.0, 4.8, 4.2, 4.9, 4.7]
    }
    
    df = pd.DataFrame(data)
    print("\nOriginal DataFrame:")
    print(df)
    
    # Advanced Aggregation: Department ke hisaab se salary ka sum & average, aur rating ka max nikalna
    aggregations = {
        'salary': ['sum', 'mean', 'count'],
        'rating': 'max'
    }
    
    print("\nPerforming Groupby Aggregation...")
    result_df = perform_advanced_aggregation(df, group_by_cols=['department'], agg_dict=aggregations)
    
    print("\nAggregated Result DataFrame:")
    print(result_df)