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
        template="skalagrad_theme"
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

def render_rating_convergence(rating_convergence_data: pd.DataFrame):
    """
    Plots rating_change vs match_number with a LOWESS trendline.
    """

    # Create scatter plot
    fig = px.scatter(
        rating_convergence_data,
        x="match_number",
        y="rating_change",
        template="skalagrad_theme"
    )

    trend_x, trend_y = plot_helpers.custom_lowess(rating_convergence_data['match_number'].values, rating_convergence_data['rating_change'].values, n_exact=4)

    # Add LOWESS trendline as a separate go.Scatter trace
    fig.add_trace(
        go.Scatter(
            x=trend_x,
            y=trend_y,
            mode='lines',
            line=dict(color='red', width=3),
            name='LOWESS Trend'
        )
    )
    # Apply watermark
    fig = style.add_watermark(fig)

    return fig

def render_matchmaking_convergence(matchmaking_convergence_data: pd.DataFrame):
    fig = px.scatter(
        matchmaking_convergence_data, 
        x="match_number", 
        y="team_score_ratio", 
        template="skalagrad_theme",
        trendline="lowess",
        trendline_options=dict(frac=0.1)
        )
    if len(fig.data) > 1:
        fig.data[1].line.color = "red"   # set trendline color
        fig.data[1].line.width = 3        # make it thicker
        fig.data[1].name = "LOWESS Trend"

    fig.add_hline(y=7/13, line_dash="dash", line_color="red", annotation_text="Optimal Match", annotation_position="top left")
    return style.add_watermark(fig)

#assemble tab

def render(data: Dict[str, pd.DataFrame]):
    content=[
        dbc.Row([
            dbc.Col(dcc.Graph(id="matchmaking1", figure=render_matchmaking_convergence(data["matchmaking_convergence"])), width=6),
            dbc.Col(dcc.Graph(id="matchmaking2", figure=render_matchmaking_convergence(data["matchmaking_convergence"])), width=6)
        ], className="tab-row")
    ]
    return html.Div(content)