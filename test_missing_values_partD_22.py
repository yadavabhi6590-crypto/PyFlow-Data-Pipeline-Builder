import pandas as pd
from pyflow.utils import handle_missing_values

if __name__ =="__main__":
    print("Missing value handler Test----")

    #step 1 To create a smaple dataframe those have some values as NaN (missing)

    data={
        "emp_id":[101,102,103,104,105],
        'salary':[50000,60000,None,75000,62000],
        'department':['HR',None,'IT','Finance','HR'],
        'rating':[4.5,4.0,3.8,None,4.3]
    }

    df=pd.DataFrame(data)
    print("Original Datafram (with missing values)")

    print(df)

   # call the missing values
    cleaned_df=handle_missing_values(df,strategy="auto")

print("cleaned dataframe (after smart imputation)")
print(cleaned_df) 