import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
import src.dashboard.style as style
import pandas as pd
from dash_extensions.enrich import DashProxy, Serverside, Trigger
from typing import Dict
import statsmodels.api as sm
import plotly.graph_objects as go
import numpy as np


#loading and caching, not used for now

def get_cached_data(engine):
    daily_matches = pd.DataFrame()
    return Serverside({"daily_matches": daily_matches})

def render_cached(data):
    daily_matches = data["daily_matches"]
    print(daily_matches)
    content=[
        dbc.Row([
            dbc.Col(dcc.Graph(id="overview1", figure=style.add_watermark(px.scatter(daily_matches, x="date", y="match_count", color="region", template="skalagrad_theme"))), width=6),
            dbc.Col(dcc.Graph(id="overview2", figure=style.add_watermark(px.scatter(daily_matches, x="date", y="match_count", template="skalagrad_theme"))), width=6)
        ], className="tab-row"),
        dbc.Row([
            dbc.Col(dcc.Graph(id="overview3", figure=style.add_watermark(px.scatter(daily_matches, x="date", y="match_count", template="skalagrad_theme"))), width=6),
            dbc.Col(dcc.Graph(id="overview4", figure=style.add_watermark(px.scatter(daily_matches, x="date", y="match_count", template="skalagrad_theme"))), width=6)
        ], className="tab-row")
    ]
    return html.Div(content)