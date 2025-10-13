from dash import dcc, html, ClientsideFunction, Dash
import dash_auth 
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import src.dashboard.style as style
from src.dashboard.components.ui_helpers import create_tab
from src.dashboard.components import overview_tab, rating_metrics_tab, matchmaking_metrics_tab, player_metrics_tab, team_metrics_tab, feature_analysis_tab, playstyle_clusters_tab, match_prediction_tab
from dash_extensions.enrich import DashProxy, Serverside, Trigger
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import logging
from src.utils.helpers import setup_logging
from datetime import datetime
import src.preprocessing.preprocessing as preprocessing

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 3306))  # default to 3306 if missing
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", pool_pre_ping=True)

setup_logging()

style.init()

dashboard_data = preprocessing.get_processed_data(engine)

app = Dash(__name__, url_base_pathname="/analytics/", external_stylesheets=[dbc.themes.BOOTSTRAP], title="Skalagrad Analytics", update_title=None)
app.title = "Skalagrad Analytics"  # ensure static title
app.server.secret_key = "some-random-secret-value" #os.getenv("DASH_SECRET_KEY", "super-secret-key")

tabs = [
    create_tab("Overview", "overview", html.Div(id="overview-tab", children=overview_tab.render(dashboard_data["overview_data"]))),
    create_tab("Rating Metrics", "rating-metrics", html.Div(id="rating-metrics-tab", children=rating_metrics_tab.render(dashboard_data["rating_metrics_data"]))),
    create_tab("Matchmaking Metrics", "matchmaking-metrics", html.Div(id="matchmaking-metrics-tab", children=matchmaking_metrics_tab.render(dashboard_data["matchmaking_metrics_data"])))
]

app.layout = html.Div([
    # Floating video logo
    html.Video(
        src="/analytics/assets/SkalaLogo.mp4",
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

if __name__ == "__main__":
    app.run(debug=True, dev_tools_ui=False, host="localhost", port=8050)

"""html.Video(
    id="video-bg",
    src="/assets/SkalaBackground.mp4",
    autoPlay=True,
    loop=True,
    muted=True
),"""    