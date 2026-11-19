import pandas as pd
from pyflow.utils import detect_and_remove_outliers

if __name__ =="__main__":
    print("--Outlier Detection & Removal Test---")

    # sample data those have extreme outliees 
    data={
        'emp_id':[1,2,3,4,5,6],
        'salary':[50000,520000,48000,530000,510000,50000000],
        'age':[25,35,30,22,27,120]
    }
    df=pd.DataFrame(data)
    print("Original DataFrame (with Outliers)")
    print(df)

    cleaned_df=detect_and_remove_outliers(df,columns=['salary','age'])

    print("Cleaned Datafram (after outlier removel)")
    print(cleaned_df)