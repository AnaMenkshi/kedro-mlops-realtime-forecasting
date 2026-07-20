import os
from pathlib import Path
import sys

import dash
import dash_bootstrap_components as dbc
import yaml
from dash import Input, Output, callback, dcc, html

# Project root and config
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root / "src"))
os.chdir(project_root)

from app_ui.utils import load_data, create_figure

with open(project_root / "conf" / "base" / "parameters.yml") as f:
    config = yaml.safe_load(f)["ui"]

ACTUAL_DATA_PATH = project_root / config["actual_data_path"]
PREDICTIONS_PATH = project_root / config["predictions_path"]

# App layout
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dcc.Interval(id="interval", interval=config["update_interval_ms"], n_intervals=0),
    dbc.Row([
        # Sidebar
        dbc.Col([
            html.H4("Control Panel", style={"color": "#222"}),
            html.Div([
                html.Label("Plots display time (last N hours)", style={"color": "#222"}),
                dcc.Input(id="lookback-hours", type="number", min=1, step=1,
                          value=config["default_lookback_hours"], style={"width": "100%"}),
            ], className="card"),
            html.Div([
                html.H5("Pipeline", style={"marginTop": "8px", "color": "#222"}),
                html.Table([
                    html.Tr([html.Td("Model", style={"color": "#666", "paddingRight": "12px"}), html.Td("CatBoost", style={"color": "#222"})]),
                    html.Tr([html.Td("Target", style={"color": "#666", "paddingRight": "12px"}), html.Td("Bike count, t+1h", style={"color": "#222"})]),
                    html.Tr([html.Td("Inference", style={"color": "#666", "paddingRight": "12px"}), html.Td("Streaming batch", style={"color": "#222"})]),
                    html.Tr([html.Td("Orchestration", style={"color": "#666", "paddingRight": "12px"}), html.Td("Kedro", style={"color": "#222"})]),
                ], style={"fontSize": "14px", "borderSpacing": "0 6px"}),
            ], className="card card-margin-top"),
        ], width=3, style={"paddingTop": "10px"}),
        # Main chart
        dbc.Col([
            html.H5("Real-time Bike Count Predictions", style={"color": "#222", "fontSize": "28px"}),
            dcc.Graph(id="graph", style={"backgroundColor": "#fff", "borderRadius": "12px", "padding": "8px"}),
        ], width=9, style={"paddingTop": "10px"}),
    ], align="start"),
], fluid=True, style={"backgroundColor": "#e9e9f0", "minHeight": "100vh", "padding": "20px"})


@callback(
    Output("graph", "figure"), 
    [
        Input("lookback-hours", "value"), 
        Input("interval", "n_intervals")
        ]
    )
def update_graph(lookback_hours, _):
    df_actual = load_data(ACTUAL_DATA_PATH)
    df_pred = load_data(PREDICTIONS_PATH)
    # Set default lookback hours if not provided
    if not lookback_hours or lookback_hours < 1:
        lookback_hours = config["default_lookback_hours"]
    figure = create_figure(df_actual, df_pred, lookback_hours)
    return figure

server = app.server

if __name__ == "__main__":
    host = os.environ.get("DASH_HOST", "127.0.0.1")
    port = int(os.environ.get("DASH_PORT", "8050"))
    app.run(debug=True, use_reloader=False, host=host, port=port)