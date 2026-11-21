


import pandas as pd

from pyflow.utils import logger


class DataValidationError(Exception):
    pass


class DataValidator:
    def __init__(
        self,
        required_columns: list[str] | None = None,
        positive_columns: list[str] | None = None,
    ):
        self.required_columns = required_columns or []
        self.positive_columns = positive_columns or []

    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        if df is None or df.empty:
            raise DataValidationError("Validation failed: transformed DataFrame is empty.")

        missing_cols = [col for col in self.required_columns if col not in df.columns]
        if missing_cols:
            raise DataValidationError(f"Validation failed: missing required columns {missing_cols}.")

        for col in self.positive_columns:
            invalid_count = int((df[col] <= 0).sum())
            if invalid_count > 0:
                raise DataValidationError(
                    f"Validation failed: column '{col}' has {invalid_count} non-positive rows."
                )

        logger.info(f"Data validation passed | rows={len(df)}, columns={len(df.columns)}")
        return df