import argparse  # Command-line arguments parse karne ke liye
import logging  # Runtime log level set karne ke liye
from pathlib import Path  # File path handling ke liye

from pyflow.pipeline import PyflowPipeline  # Main ETL pipeline class import ki
from pyflow.utils import logger  # Existing logger import kiya


def build_parser() -> argparse.ArgumentParser:  # CLI flags aur options define karne wala helper
    parser = argparse.ArgumentParser(  # CLI parser banaya
        prog="pyflow",
        description="PyFlow NYC Taxi ETL Pipeline CLI",
    )
    parser.add_argument(  # Config file path ke liye flag
        "--config",
        default="config/pipeline.yaml",
        help="Path to YAML/JSON pipeline config (default: config/pipeline.yaml)",
    )
    parser.add_argument(  # Bina output file save kiye test run karne ke liye flag
        "--dry-run",
        action="store_true",
        help="Run extract, transform, and validation without writing output files",
    )
    parser.add_argument(  # Console/file log verbosity control karne ke liye flag
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO)",
    )
    return parser  # Configured parser return kiya


def main(argv: list[str] | None = None) -> int:  # CLI main execution function
    parser = build_parser()  # Parser banaya
    args = parser.parse_args(argv)  # Terminal arguments parse kiye

    numeric_level = getattr(logging, args.log_level.upper(), logging.INFO)  # String level ko logging constant banaya
    logger.setLevel(numeric_level)  # Logger level update kiya

    config_file = Path(args.config)  # Config path check karne ke liye Path object
    if not config_file.exists():  # Config file nahi mili toh clean error code return karega
        logger.error(f"Config file not found: {config_file}")
        return 1

    pipeline = PyflowPipeline(config_path=str(config_file))  # Pipeline instance banaya

    if args.dry_run:  # Dry-run mode mein load step skip hoga
        logger.info("Dry-run mode enabled: skipping output file writes")
        pipeline.run()
        return 0

    pipeline.run()  # Normal full ETL run
    return 0  # Success exit code


if __name__ == "__main__":  # Direct script execution par main() chalega
    raise SystemExit(main())