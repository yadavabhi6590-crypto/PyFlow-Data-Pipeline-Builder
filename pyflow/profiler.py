

import json  # Profiling report ko JSON file mein save karne ke liye
from pathlib import Path  # Output directory aur report path banane ke liye
import pandas as pd  # DataFrame summary stats nikalne ke liye

from pyflow.utils import logger  # Pipeline logger import kiya


class DataProfiler:  # DataFrame ka automated summary report banane wali class
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)  # Reports yahan save hongi

    def generate(self, df: pd.DataFrame, name: str = "dataset_profile") -> dict:
        self.output_dir.mkdir(parents=True, exist_ok=True)  # Folder na ho toh bana dega

        # Har column ki basic details aur null counts
        columns_info = {}
        for col in df.columns:
            null_count = int(df[col].isna().sum())
            null_pct = round((null_count / len(df)) * 100, 2) if len(df) > 0 else 0.0
            columns_info[col] = {
                "dtype": str(df[col].dtype),
                "null_count": null_count,
                "null_pct": null_pct,
                "unique_count": int(df[col].nunique(dropna=True)),
            }

        # Numeric columns ke liye min, max, mean aur median
        numeric_summary = {}
        numeric_cols = df.select_dtypes(include="number").columns
        for col in numeric_cols:
            series = df[col].dropna()
            if not series.empty:
                numeric_summary[col] = {
                    "min": float(series.min()),
                    "max": float(series.max()),
                    "mean": round(float(series.mean()), 4),
                    "median": round(float(series.median()), 4),
                }

        profile = {
            "dataset_name": name,
            "row_count": int(len(df)),
            "column_count": int(len(df.columns)),
            "memory_mb": round(float(df.memory_usage(deep=True).sum() / (1024 * 1024)), 2),
            "columns": columns_info,
            "numeric_summary": numeric_summary,
        }

        # JSON report save karna
        json_path = self.output_dir / f"{name}.json"
        json_path.write_text(json.dumps(profile, indent=2), encoding="utf-8")

        # Readable Markdown report save karna
        md_lines = [
            f"# Data Profile Report: {name}",
            "",
            f"- **Rows:** {profile['row_count']:,}",
            f"- **Columns:** {profile['column_count']}",
            f"- **Memory Usage:** {profile['memory_mb']} MB",
            "",
            "## Columns Overview",
            "| Column | Dtype | Nulls | Null % | Unique |",
            "| --- | --- | --- | --- | --- |",
        ]
        for col, info in columns_info.items():
            md_lines.append(
                f"| {col} | {info['dtype']} | {info['null_count']:,} | {info['null_pct']}% | {info['unique_count']:,} |"
            )

        if numeric_summary:
            md_lines.extend([
                "",
                "## Numeric Summary",
                "| Column | Min | Max | Mean | Median |",
                "| --- | --- | --- | --- | --- |",
            ])
            for col, stats in numeric_summary.items():
                md_lines.append(
                    f"| {col} | {stats['min']} | {stats['max']} | {stats['mean']} | {stats['median']} |"
                )

        md_path = self.output_dir / f"{name}.md"
        md_path.write_text("\n".join(md_lines), encoding="utf-8")

        logger.info(f"Profiling report saved to {json_path} and {md_path}")
        return {"json": str(json_path), "markdown": str(md_path)}