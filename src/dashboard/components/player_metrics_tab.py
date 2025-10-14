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

def render_player_stats_mmr_correlation(player_stats: pd.DataFrame):
    """
    Create line plots of all stats vs mmr_bin in a single figure.
    agg_stats should have columns: mmr_bin, score, kills, significant_assists, assists, teamkills
    """
    # List of stats to plot
    stats_cols = ["kills", "significant_assists", "assists", "teamkills"]
    
    # Melt the DataFrame so that Plotly can handle multiple lines
    df_melted = player_stats.melt(id_vars="mmr_bin", value_vars=stats_cols, 
                               var_name="stat", value_name="value")
    
    # Create line plot
    fig = px.line(
        df_melted,
        x="mmr_bin",
        y="value",
        color="stat",
        markers=True,
        template="skalagrad_theme",
        labels={"mmr_bin": "Rating", "value": "Value", "stat": "Stat"}
    )
    
    # Add watermark or any additional styling
    return style.add_watermark(fig)

def render_player_stats_mmr_correlation_2(player_stats: pd.DataFrame):
    """
    Create line plots of all stats vs mmr_bin in a single figure.
    agg_stats should have columns: mmr_bin, score, kills, significant_assists, assists, teamkills
    """
    # List of stats to plot
    stats_cols = ["kills", "significant_assists", "assists", "teamkills"]
    
    # Melt the DataFrame so that Plotly can handle multiple lines
    df_melted = player_stats.melt(id_vars="mmr_bin", value_vars=stats_cols, 
                               var_name="stat", value_name="value")
    
    # Create line plot
    fig = px.line(
        df_melted,
        x="mmr_bin",
        y="value",
        color="stat",
        markers=True,
        template="skalagrad_theme",
        labels={"mmr_bin": "Rating", "value": "Value", "stat": "Stat"}
    )
    
    # Add watermark or any additional styling
    return style.add_watermark(fig)

#assemble tab

def render(data: Dict[str, pd.DataFrame]):
    content=[
        dbc.Row([
            dbc.Col(dcc.Graph(id="player1", figure=render_player_stats_mmr_correlation(data["player_stats"])), width=6),
            dbc.Col(dcc.Graph(id="player2", figure=render_player_stats_mmr_correlation_2(data["player_stats_2"])), width=6)
        ], className="tab-row")
    ]
    return html.Div(content)