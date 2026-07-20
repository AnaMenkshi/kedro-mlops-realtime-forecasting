"""Tests for the pipeline registry."""
from kedro_mlops_realtime_forecasting.pipeline_registry import register_pipelines


class TestPipelineRegistry:
    def test_registers_expected_pipelines(self):
        pipelines = register_pipelines()
        assert set(pipelines) == {"__default__", "training", "inference"}

    def test_registered_pipelines_are_not_empty(self):
        pipelines = register_pipelines()
        for name, pipeline in pipelines.items():
            assert len(pipeline.nodes) > 0, f"Pipeline '{name}' has no nodes"

    def test_default_pipeline_matches_training(self):
        pipelines = register_pipelines()
        default_nodes = {node.name for node in pipelines["__default__"].nodes}
        training_nodes = {node.name for node in pipelines["training"].nodes}
        assert default_nodes == training_nodes
