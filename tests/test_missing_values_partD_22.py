import pandas as pd
from pyflow.utils import handle_missing_values


def test_handle_missing_values_auto():
    data = {
        "emp_id": [101, 102, 103, 104, 105],
        "salary": [50000, 60000, None, 75000, 62000],
        "department": ["HR", None, "IT", "Finance", "HR"],
        "rating": [4.5, 4.0, 3.8, None, 4.3],
    }
    df = pd.DataFrame(data)
    cleaned_df = handle_missing_values(df, strategy="auto")

    assert cleaned_df.isna().sum().sum() == 0
    assert cleaned_df.loc[2, "salary"] == 61000.0
    assert cleaned_df.loc[1, "department"] == "HR"


if __name__ == "__main__":
    print("Missing value handler Test----")

    data = {
        "emp_id": [101, 102, 103, 104, 105],
        "salary": [50000, 60000, None, 75000, 62000],
        "department": ["HR", None, "IT", "Finance", "HR"],
        "rating": [4.5, 4.0, 3.8, None, 4.3],
    }

    df = pd.DataFrame(data)
    print("Original Datafram (with missing values)")
    print(df)

    cleaned_df = handle_missing_values(df, strategy="auto")
    print("cleaned dataframe (after smart imputation)")
    print(cleaned_df)