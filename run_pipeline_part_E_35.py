import argparse
from pyflow.pipeline import PyflowPipeline

def parse_args():
    parser=argparse.ArgumentParser(description="Run Pyflow ETL pipeline")
    parser.add_argument(
        "--config",
        default="config/pipeline.yaml",
        help="Path to pipeline YAML or JSOn config file"
    )
    return parser.parse_args()

if __name__=="__main__":
    args=parse_args()
    pipeline=PyflowPipeline(config_path=args.config)
    outputs =pipeline.run()
    print("Generated outputs",outputs)