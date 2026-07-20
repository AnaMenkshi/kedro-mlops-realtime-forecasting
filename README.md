# kedro-mlops-realtime-forecasting

[![Powered by Kedro](https://img.shields.io/badge/powered_by-kedro-ffc900?logo=kedro)](https://kedro.org)

An MLOps pipeline for hourly bike-share demand forecasting, built on [Kedro](https://kedro.org). The pipeline covers feature engineering, model training, and batch inference, with a [Dash](https://dash.plotly.com/) dashboard for monitoring predictions against actuals in real time.

## Architecture

The project is organized into three Kedro pipelines, orchestrated independently:

| Pipeline | Responsibility |
|---|---|
| `feature_eng` | Column renaming and lag-feature generation from raw hourly data |
| `training` | Target construction, train/test split, model fitting, evaluation, and persistence |
| `inference` | Model loading, batch prediction, and timestamp alignment |

Three entrypoint scripts drive the pipelines outside of `kedro run`:

- `entrypoints/training.py` — runs the training pipeline once
- `entrypoints/inference.py` — replays historical data in fixed-size batches at a configurable interval, simulating a streaming inference workload
- `entrypoints/app_ui.py` — serves the Dash dashboard, reading predictions and actuals as they're written

The three components run as independent services, communicating through `data/` and `conf/` as shared state — model artifacts, prediction output, and configuration flow between them without direct coupling.

## Model

The training pipeline supports three interchangeable regressors, selected via `training.model_type` in `conf/base/parameters.yml`:

- `catboost` (default) — gradient-boosted trees, native lag-feature handling
- `random_forest`
- `linear_regression`

Model hyperparameters are defined per algorithm under `training.model_params` in the same file.

## Tech stack

Python 3.12–3.13 · Kedro · CatBoost / scikit-learn · pandas · Dash · Plotly · Docker Compose

## Project structure

```
├── conf/base/            # Pipeline parameters and data catalog
├── conf/local/           # Machine-specific overrides and credentials (not tracked)
├── data/                 # Raw data, intermediate artifacts, trained models, predictions
├── docs/                 # Sphinx API documentation
├── entrypoints/          # Standalone scripts for training, inference, and the dashboard
├── notebooks/            # Exploratory analysis and model development notes
├── src/kedro_mlops_realtime_forecasting/   # Pipeline definitions and node functions
├── src/app_ui/           # Dash application
└── tests/                # Unit tests
```

## Setup

Requires Python 3.12 or 3.13.

```bash
python -m venv .venv
source .venv/bin/activate      # .venv\Scripts\activate on Windows
pip install -e .
```

This repository does not include the dataset or a trained model — `data/` is excluded via `.gitignore`. To run the pipeline, populate `data/01_raw/` with the source parquet files referenced in `conf/base/catalog.yml` (the [UCI Bike Sharing dataset](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset), hourly resolution).

## Usage

Train a model:

```bash
python entrypoints/training.py
```

Run the inference loop (replays historical data and writes predictions continuously):

```bash
python entrypoints/inference.py
```

Launch the dashboard in a separate process:

```bash
python entrypoints/app_ui.py
```

The dashboard is available at `http://localhost:8050` and refreshes automatically as new predictions are written.

### Docker

```bash
docker compose up
```

Runs training, inference, and the dashboard as three services with shared volumes for data and configuration.

## Configuration

- `conf/base/catalog.yml` — data source and artifact locations
- `conf/base/parameters.yml` — feature engineering, training, and inference parameters
- `conf/local/` — local overrides and credentials, excluded from version control

## Testing

```bash
pytest
```

## Documentation

API documentation is generated with Sphinx from `docs/source/`. Build with:

```bash
pip install -e ".[docs]"
sphinx-build docs/source docs/build
```
