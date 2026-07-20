"""Unit tests for pipeline node functions."""
import pandas as pd

from kedro_mlops_realtime_forecasting.pipelines.nodes import (
    rename_columns,
    make_target,
    compute_metrics,
)


class TestRenameColumns:
    def test_renames_specified_columns(self):
        df = pd.DataFrame({"cnt": [1, 2, 3], "temp": [0.1, 0.2, 0.3]})
        result = rename_columns(df, {"cnt": "bike_count", "temp": "temperature"})
        assert list(result.columns) == ["bike_count", "temperature"]

    def test_leaves_unmapped_columns_untouched(self):
        df = pd.DataFrame({"cnt": [1], "datetime": ["2012-01-01"]})
        result = rename_columns(df, {"cnt": "bike_count"})
        assert "datetime" in result.columns


class TestMakeTarget:
    def test_shifts_target_column_forward(self):
        df = pd.DataFrame({"bike_count": [10, 20, 30, 40]})
        params = {
            "shift_period": 1,
            "target_column": "bike_count",
            "new_target_name": "target",
        }
        result = make_target(df, params)
        assert result["target"].tolist() == [20, 30, 40, 40]


class TestComputeMetrics:
    def test_perfect_predictions_have_zero_error(self):
        y_true = [10, 20, 30]
        y_pred = [10, 20, 30]
        metrics = compute_metrics(y_true, y_pred)
        assert metrics["MAE"] == 0.0
        assert metrics["RMSE"] == 0.0

    def test_returns_expected_keys(self):
        metrics = compute_metrics([1, 2, 3], [1, 2, 4])
        assert set(metrics) == {"MAE", "RMSE", "MAPE"}
