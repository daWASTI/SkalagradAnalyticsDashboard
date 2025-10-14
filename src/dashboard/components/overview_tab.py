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
from src.dashboard.components.figures import plot_helpers

#render figures

def render_daily_matches(daily_matches_data: pd.DataFrame):
    fig = px.line(
        daily_matches_data, 
        x="date", 
        y="match_count",
        template="skalagrad_theme",
        title='Matches Per Day'
        )
    return style.add_watermark(fig)

def render_user_count(user_count_data: pd.DataFrame):
    user_count_long = user_count_data.melt(
        id_vars='date', 
        value_vars=['players_1d', 'players_7d', 'players_30d', 'total_users'],
        var_name='window',
        value_name='active_players'
    )

    # Rename for nicer legend labels
    user_count_long['window'] = user_count_long['window'].replace({
        'players_1d': '1-Day Active',
        'players_7d': '7-Day Active',
        'players_30d': '30-Day Active'
    })

    # Plot
    fig = px.line(
        user_count_long,
        x='date',
        y='active_players',
        color='window',
        template="skalagrad_theme",
        title='Active Players Over Time'
    )
    return style.add_watermark(fig)

#assemble tab

def render(data: Dict[str, pd.DataFrame]):
    content=[
        dbc.Row([
            dbc.Col(dcc.Graph(id="overview1", figure=render_daily_matches(data["daily_matches"])), width=6),
            dbc.Col(dcc.Graph(id="overview2", figure=render_user_count(data["user_count"])), width=6)
        ], className="tab-row")
    ]
    return html.Div(content)