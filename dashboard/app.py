from dash import dcc, html, ClientsideFunction
import dash_auth 
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dashboard.style as style
from dashboard.components.ui_helpers import create_tab
from dashboard.components import overview_tab, player_metrics_tab, team_metrics_tab, feature_analysis_tab, playstyle_clusters_tab, match_prediction_tab, rating_metrics_tab
from dash_extensions.enrich import DashProxy, Serverside, Trigger
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import logging
from src.utils.helpers import setup_logging
from datetime import datetime

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 3306))  # default to 3306 if missing
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", pool_pre_ping=True)

setup_logging()

style.init()

VALID_USERNAME_PASSWORD_PAIRS = {
    #os.getenv("DASH_USER"): os.getenv("DASH_PASSWORD")
    'dawasti': '1234'
}

app = DashProxy(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True, title="Skalagrad Analytics", update_title=None)
app.title = "Skalagrad Analytics"  # ensure static title
app.server.secret_key = "some-random-secret-value" #os.getenv("DASH_SECRET_KEY", "super-secret-key")
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

tabs = [
    create_tab("Overview", "overview", html.Div(id="overview-tab", children=overview_tab.render(engine))),
    create_tab("Rating Metrics", "rating_metrics", html.Div(id="rating-metrics-tab", children=rating_metrics_tab.render(engine))),
    create_tab("Matchmaking Metrics", "matchmaking_metrics", html.Div(id="matchmaking-metrics-tab", children=match_prediction_tab.render(match_prediction_tab.dummy_data))),
    create_tab("Player Metrics", "player_metrics", html.Div(id="player-metrics-tab", children=overview_tab.render(engine))),
    create_tab("Team Metrics", "team_metrics", html.Div(id="team-metrics-tab", children=team_metrics_tab.render(team_metrics_tab.dummy_data))),
    create_tab("Feature Analysis", "feature_analysis", html.Div(id="feature-analysis-tab", children=feature_analysis_tab.render(feature_analysis_tab.dummy_data))),
    create_tab("Playstyle Clusters", "playstyle_clusters", html.Div(id="playstyle-clusters-tab", children=playstyle_clusters_tab.render(playstyle_clusters_tab.dummy_data))),
    create_tab("Match Prediction", "match_prediction", html.Div(id="match-prediction-tab", children=match_prediction_tab.render(match_prediction_tab.dummy_data))),
    create_tab("Live", "live", html.Div(id="live-tab", children=match_prediction_tab.render(match_prediction_tab.dummy_data)))
]

app.layout = html.Div([
    # Floating video logo
    html.Video(
        src="/assets/SkalaLogo.mp4",
        autoPlay=True,
        loop=True,
        muted=True,
        style={
            "position": "absolute",
            "top": "10px",
            "left": "10px",
            "width": "250px",
            "height": "250px",
            "zIndex": "1000"
        }
    ),

    # Main container with header and tabs
    dbc.Container([
        dcc.Store(id="store-data"),
        dcc.Interval(id="interval", interval=10*1000, n_intervals=0),
        dbc.Row([
            dbc.Col(
                html.H1("Skalagrad Analytics Dashboard"),
                width=12,
                style={"color": style.SKALA_YELLOW}
            )
        ]),

        # Tabs go here
        dbc.Tabs(id="tabs", active_tab="overview", children=tabs),

        # Content area that updates from callback
        html.Div(id="tab-content")

    ])

])

# --- Callback: load per-tab data ---
@app.callback(
    Output("store-data", "data"),
    Input("interval", "n_intervals"),
    Input("tabs", "active_tab")
)
def load_data(_, active_tab):
    """
    Loads cached data for the currently active tab.
    Uses Serverside caching to avoid sending large DataFrames to the browser.
    """
    if active_tab == "overview":
        x = overview_tab.get_cached_data(engine)
        #print(x)
        return x
    elif active_tab == "player_metrics":
        return player_metrics_tab.get_cached_data(engine)
    elif active_tab == "team_metrics":
        return team_metrics_tab.get_cached_data(engine)
    elif active_tab == "feature_analysis":
        return feature_analysis_tab.get_cached_data(engine)
    elif active_tab == "playstyle_clusters":
        return playstyle_clusters_tab.get_cached_data(engine)
    elif active_tab == "match_prediction":
        return match_prediction_tab.get_cached_data(engine)
    return Serverside(None)

# --- Callbacks: update each tab’s inner div ---
@app.callback(
    Output("overview-tab", "children"),
    Input("store-data", "data")
)
def update_overview(data):
    if data is None:
        return "Loading..."
    return overview_tab.render(data)


@app.callback(
    Output("player-metrics-tab", "children"),
    Input("store-data", "data")
)
def update_player_metrics(data):
    if data is None:
        return "Loading..."
    return player_metrics_tab.render(data)


@app.callback(
    Output("team-metrics-tab", "children"),
    Input("store-data", "data")
)
def update_team_metrics(data):
    if data is None:
        return "Loading..."
    return team_metrics_tab.render(data)


@app.callback(
    Output("feature-analysis-tab", "children"),
    Input("store-data", "data")
)
def update_feature_analysis(data):
    if data is None:
        return "Loading..."
    return feature_analysis_tab.render(data)


@app.callback(
    Output("playstyle-clusters-tab", "children"),
    Input("store-data", "data")
)
def update_playstyle_clusters(data):
    if data is None:
        return "Loading..."
    return playstyle_clusters_tab.render(data)


@app.callback(
    Output("match-prediction-tab", "children"),
    Input("store-data", "data")
)
def update_match_prediction(data):
    if data is None:
        return "Loading..."
    return match_prediction_tab.render(data)

if __name__ == "__main__":
    app.run(debug=True, dev_tools_ui=False, host="localhost", port=8050)

"""html.Video(
    id="video-bg",
    src="/assets/SkalaBackground.mp4",
    autoPlay=True,
    loop=True,
    muted=True
),"""    