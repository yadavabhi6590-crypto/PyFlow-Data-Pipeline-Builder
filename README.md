# PyFlow --- Python ETL Data Pipeline Builder

A configurable Python project for extracting, transforming, validating,
profiling, and exporting tabular data. PyFlow is being developed as a
modular ETL framework using Python and Pandas, with a focus on practical
data-engineering concepts such as reusable components,
configuration-driven workflows, logging, and automated tests.

> **Project status:** Development / portfolio project. Run the setup and
> verification steps below in your environment before treating the
> pipeline or every listed file format as production-ready.

## Overview

ETL stands for **Extract, Transform, Load**:

1.  **Extract** data from a configured source file.
2.  **Transform** the extracted DataFrame using cleaning and preparation
    steps.
3.  **Validate** the transformed data against configured quality rules.
4.  **Profile** the data and generate summary reports when profiling is
    enabled.
5.  **Load** the result into configured output formats.

The current pipeline configuration is `config/pipeline.yaml`. The
pipeline is orchestrated by `PyflowPipeline` in `pyflow/pipeline.py`.

## Project goals

- Organize ETL functionality into reusable Python modules.
- Read pipeline settings from YAML or JSON configuration files.
- Work with tabular datasets using Pandas.
- Apply common data-cleaning operations such as missing-value removal,
  deduplication, datetime parsing, and query filtering.
- Validate required columns and positive-value constraints before
  loading.
- Export processed data to supported output formats.
- Record pipeline activity using application logging.
- Practice automated testing with Pytest.

## Technology stack

- **Python** --- application logic and orchestration
- **Pandas** --- tabular data processing
- **PyYAML** --- YAML configuration parsing
- **PyArrow** --- Parquet input/output support
- **OpenPyXL** --- Excel file support through Pandas
- **pytest** --- automated tests
- **tqdm** --- pipeline progress display
- **watchdog** --- file-system monitoring exercises
- **chardet** --- file-encoding detection exercises

See [`requirements.txt`](requirements.txt) for the dependency list.

## Repository structure

```text
PyFlow-Data-Pipeline-Builder/
│
├── config/
│   ├── config.json
│   ├── config.yaml
│   └── pipeline.yaml
│
├── logs/
│   └── pipeline.log
│
├── pyflow/
│   ├── __init__.py
│   ├── config.py
│   ├── extractors.py
│   ├── loaders.py
│   ├── pipeline.py
│   ├── profiler.py
│   ├── transformeres.py
│   ├── utils.py
│   └── validators.py
│
├── reports/
│   ├── nyc_taxi_clean_profile.json
│   ├── nyc_taxi_clean_profile.md
│   ├── test_profile.json
│   └── test_profile.md
│
├── tests/
│   └── test_*.py
│
├── cli.py
├── conftest.py
├── main.py
├── requirements.txt
└── .gitignore
```

> The transformer module is currently named `transformeres.py` in this
> source version. If you rename it to `transformers.py`, update the
> imports in `pipeline.py` and any tests or scripts that reference the
> old name.

## Current components

---

Component File Responsibility

---

Configuration `pyflow/config.py` Loads YAML/JSON
settings and provides
section/key access

Extraction `pyflow/extractors.py` Reads source data into
a Pandas DataFrame

Transformation `pyflow/transformeres.py` Provides DataFrame
cleaning and filtering
methods

Validation `pyflow/validators.py` Checks empty data,
required columns, and
positive-value rules

Loading `pyflow/loaders.py` Exports a DataFrame to
configured output
formats

Orchestration `pyflow/pipeline.py` Coordinates the ETL
stages

Profiling `pyflow/profiler.py` Generates JSON and
Markdown data-profile
reports

Utilities `pyflow/utils.py` Shared helpers,
logging, and utility
functions

CLI `cli.py` Accepts configuration
and logging options

Tests `tests/` Contains focused tests
for assignment
functionality

---

## Configuration

The default pipeline configuration is `config/pipeline.yaml`.

The current configuration uses these sections:

- `extract`: input directory, file name, and optional file type
- `transform`: datetime column, columns used for missing-value
  removal, deduplication, and query filter
- `load`: output directory, output file name, export formats, and
  index option
- `profile`: whether to generate a profile and where to save it

Example:

```yaml
extract:
  base_dir: "data"
  file_name: "your_input_file.csv"
  file_type: null

transform:
  datetime_col: "your_datetime_column"
  drop_missing_subset:
    - "required_column"
  deduplicate: true
  filter_query: "numeric_column > 0"

load:
  output_dir: "output"
  file_name: "processed_data"
  formats:
    - "csv"
    - "parquet"
    - "json"
  index: false

profile:
  enabled: true
  output_dir: "reports"
  report_name: "dataset_profile"
```

Replace the example column names with columns that exist in your
dataset. Place the input file in the configured `base_dir`.

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/<your-github-username>/PyFlow-Data-Pipeline-Builder.git
cd PyFlow-Data-Pipeline-Builder
```

Replace `<your-github-username>` with your GitHub username.

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Add an input dataset

Create a `data/` directory and place your input file inside it. Update
`extract.file_name` and the transformation column names in
`config/pipeline.yaml` to match the dataset.

### 5. Run the pipeline

```bash
python cli.py --config config/pipeline.yaml
```

The CLI also accepts a logging level:

```bash
python cli.py --config config/pipeline.yaml --log-level DEBUG
```

The `--dry-run` option is present in the current CLI source, but its
behavior should be verified and corrected before relying on it: the
current implementation calls the regular pipeline run path.

## Run tests

From the repository root:

```bash
pytest -v
```

To run one test module:

```bash
pytest -v tests/test_pyflow.py
```

A test file being present does not by itself mean the test suite passes.
Record the actual test result from your machine and add it to this
README only after running the tests successfully.

## Outputs

Depending on the active configuration and successful execution, PyFlow
is intended to create:

- Processed output files in the configured output directory.
- Application logs in the configured log location.
- Data profiling reports in JSON and Markdown formats.

Generated files and reports should be checked after each run. Do not
commit large source datasets, private data, local database files,
virtual environments, or temporary cache files.

## Data sources for practice

The assignment references these public datasets:

- [NYC Taxi & Limousine Commission trip record
  data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- [The New York Times COVID-19 data
  repository](https://github.com/nytimes/covid-19-data)
- [GDP
  dataset](https://github.com/datasets/gdp/blob/main/data/gdp.csv)
- Bonus: OpenFlights airport and airline data

Follow each source's terms and data-use guidance. The project repository
should contain only appropriately licensed data and preferably small
synthetic or sample files for reproducible demonstrations.

## Development notes

This repository is an educational and portfolio project. Before
presenting it as a complete or production-ready ETL framework:

1.  Verify each extractor and loader format with representative sample
    files.
2.  Correct and test chunked CSV processing and nested JSON flattening.
3.  Verify Excel sheet merging and the CLI dry-run behavior.
4.  Validate all configuration files and ensure the configured input
    dataset exists.
5.  Run the complete test suite and record the real result.
6.  Review logging, retry behavior, and data-validation edge cases.
7.  Remove generated caches and local-only artifacts from version
    control.

## Roadmap

- [ ] Verify CSV, JSON, Excel, and Parquet extraction paths
- [ ] Verify large-file chunk processing
- [ ] Complete and test nested JSON flattening
- [ ] Complete and test Excel sheet merging
- [ ] Verify transformation and validation edge cases
- [ ] Verify CLI dry-run behavior
- [ ] Add reproducible sample input data
- [ ] Run and document the full Pytest suite
- [ ] Add screenshots of pipeline execution, test results, and
      generated reports

## Author

**Abhishek Yadav**

BCA Graduate \| Python & Data Engineering Enthusiast

- GitHub: \[https://github.com/yadavabhi6590-crypto\]
- LinkedIn: \[https://www.linkedin.com/in/abhishek-yadav-465960310/\]

## Acknowledgements

Created as a hands-on Python for Data Engineering assignment to practice
ETL design, data processing, validation, configuration management,
logging, and testing.
