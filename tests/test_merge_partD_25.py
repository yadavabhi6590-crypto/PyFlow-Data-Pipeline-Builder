

import pandas as pd
from pyflow.utils import marge_dataframes


if __name__ =="__main__":
    print("__Dataframe Merge & Concat Test")

    # Test 1 vetical Concatenation (Axis =0)

    df1=pd.DataFrame({'id':[1,2],'name':['Anshu','Abhishek']})
    df2=pd.DataFrame({'id':[3,4],'name':['avaya','abhi']})

    print("Vertical concatenation result")

    concatenated_df= marge_dataframes([df1,df2],axis=0)

    print(concatenated_df)

    # 2 Horizontal merge / join(axis=1)
    df_emp=pd.DataFrame({'emp_id':[101,102,103],'department': ['IT', 'HR', 'Finance']})
    df_sal = pd.DataFrame({'emp_id': [101, 102, 104], 'salary': [50000, 60000, 55000]})
    
    print("\n2. Horizontal Inner Join Result:")
    merged_df = marge_dataframes([df_emp, df_sal], how='inner', on='emp_id', axis=1)
    print(merged_df)