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

def render_score_mmr_correlation(player_stats: pd.DataFrame):
    
    player_stats = player_stats.rename(columns={"team_score_ratio_group":"Match outcome", "mmr_bin":"rating"})

    player_stats['Match outcome'] = player_stats['Match outcome'].replace({
        '< 0.8': 'Close',
        '>= 0.8': 'Decisive'
    })

    # Create line plot
    fig = px.line(
        player_stats,
        x="rating",
        y="score",
        color="Match outcome",
        template="skalagrad_theme",
        title="Average score per round vs rating"
    )
    
    # Add watermark or any additional styling
    return style.add_watermark(fig)

def render_kills_mmr_correlation(player_stats: pd.DataFrame):

    player_stats = player_stats.rename(columns={"team_score_ratio_group":"Match outcome", "mmr_bin":"rating"})

    player_stats['Match outcome'] = player_stats['Match outcome'].replace({
        '< 0.8': 'Close',
        '>= 0.8': 'Decisive'
    })
    
    # Create line plot
    fig = px.line(
        player_stats,
        x="rating",
        y="kills",
        color="Match outcome",
        template="skalagrad_theme",
        title="Average kills per round vs rating"
    )
    
    # Add watermark or any additional styling
    return style.add_watermark(fig)

def render_significant_assists_mmr_correlation(player_stats: pd.DataFrame):

    player_stats = player_stats.rename(columns={"team_score_ratio_group":"Match outcome", "mmr_bin":"rating"})

    player_stats['Match outcome'] = player_stats['Match outcome'].replace({
        '< 0.8': 'Close',
        '>= 0.8': 'Decisive'
    })
    
    # Create line plot
    fig = px.line(
        player_stats,
        x="rating",
        y="significant_assists",
        color="Match outcome",
        template="skalagrad_theme",
        title="Average significant assists per round vs rating"
    )
    
    # Add watermark or any additional styling
    return style.add_watermark(fig)

def render_assists_mmr_correlation(player_stats: pd.DataFrame):

    player_stats = player_stats.rename(columns={"team_score_ratio_group":"Match outcome", "mmr_bin":"rating"})

    player_stats['Match outcome'] = player_stats['Match outcome'].replace({
        '< 0.8': 'Close',
        '>= 0.8': 'Decisive'
    })
    
    # Create line plot
    fig = px.line(
        player_stats,
        x="rating",
        y="assists",
        color="Match outcome",
        template="skalagrad_theme",
        title="Average assists per round vs rating"
    )
    
    # Add watermark or any additional styling
    return style.add_watermark(fig)

#assemble tab

def render(data: Dict[str, pd.DataFrame]):
    content=[
        dbc.Row([
            dbc.Col(dcc.Graph(id="player1", figure=render_score_mmr_correlation(data["player_stats"])), width=6),
            dbc.Col(dcc.Graph(id="player2", figure=render_kills_mmr_correlation(data["player_stats"])), width=6)
        ], className="tab-row"),
        dbc.Row([
            dbc.Col(dcc.Graph(id="player3", figure=render_significant_assists_mmr_correlation(data["player_stats"])), width=6),
            dbc.Col(dcc.Graph(id="player4", figure=render_assists_mmr_correlation(data["player_stats"])), width=6)
        ], className="tab-row")
    ]
    return html.Div(content)