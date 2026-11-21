


import pandas as pd
import pytest

from pyflow.transformers import dataTransformer
from pyflow.loaders import Dataloader
from pyflow.utils import retry_with_backoff

def test_transformer_cleaning_and_filter():
    sample_df =pd.DataFrame({
        "passenger_count":[1.0,None,2.0,2.0],
        "fare_amount":[15.0,10.0,12.0,12.0],
    })
    transformer =dataTransformer(sample_df)
    transformer.drop_missing(subset=["passenger_count"])
    transformer.remove_duplicates()
    transformer.filter_query("fare_amount >10")

    result_df =transformer.get_df()
    assert len(result_df) ==2

    def test_loader_saves_csv_and_parquer(tem_path):
        df=pd.DataFrame({
            "vendor_if":[1,2],
            "fare_amount":[20.5,35.0]
        })

        loader=Dataloader(output_dir=str(tmp_path))
        saved=loader.load(
            df=df,
            file_name="test_trips",
            formats=["csv","parquet"],
            index=False,
        )
        assert "csv"in saved
        assert "parquet" in saved 
        assert(tem_path/"test_trips.csv").exists()
        assert(tem_path/"test_trips.parquet").exists()

    def test_retry_with_backoff_recovers():
        attempts={"count":0}

        @retry_with_backoff(max_retries=3,base_delay=0.01,backoff_factor=2.0)
        def flaky_step():
            attempts["count"]+=1
            if attempts["count"]<3:
                raise IOError("temporary file busy")

        assert flaky_step()=="ok"
        assert attempts["count"]==3
    def test_retry_with_backoff_raises_after_max_retries():
        @retry_with_backoff(max_retries=1,base_delay=0.01,backoff_factor=2.0)
        def always_fails():
            raise ValueError("Permanent error")

        with pytest.raises(ValueError):
            always_fails()