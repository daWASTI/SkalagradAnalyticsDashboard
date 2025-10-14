import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
import src.dashboard.style as style
from src.dashboard.components.figures.plot_helpers import custom_lowess
import pandas as pd
from typing import Dict
import statsmodels.api as sm
import plotly.graph_objects as go
import numpy as np

#render figures

def render_matchmaking_convergence(matchmaking_convergence_data: pd.DataFrame):
    """
    Plots rating_change vs match_number with a LOWESS trendline.
    The first `n_exact` points are matched exactly, the rest is smoothed.
    
    Parameters:
    - rating_convergence_data: DataFrame with 'match_number' and 'rating_change'
    - n_exact: number of points at the start to match exactly
    """

    x = matchmaking_convergence_data['match_number'].values
    y = matchmaking_convergence_data['team_score_ratio'].values

    trend_x, trend_y = custom_lowess(x, y, n_exact=0)

    # Create scatter plot
    fig = px.scatter(
        matchmaking_convergence_data,
        x="match_number",
        y="team_score_ratio",
        template="skalagrad_theme"
    )

    # Add LOWESS trendline as a separate go.Scatter trace
    fig.add_trace(
        go.Scatter(
            x=trend_x,
            y=trend_y,
            mode='lines',             # ensures the line is drawn
            line=dict(color='red', width=3),
            name='LOWESS Trend'
        )
    )

    # Add horizontal line 
    fig.add_hline(
        y=7/13,
        line=dict(color='red', width=2, dash='dash'),
        annotation_text="Ideal Match",
        annotation_position="top left"
    )

    # Apply watermark
    fig = style.add_watermark(fig)

    return fig

#assemble tab

def render(data: Dict[str, pd.DataFrame]):
    content=[
        dbc.Row([
            dbc.Col(dcc.Graph(id="matchmaking1", figure=render_matchmaking_convergence(data["matchmaking_convergence"])), width=6),
            dbc.Col(dcc.Graph(id="matchmaking2", figure=render_matchmaking_convergence(data["matchmaking_convergence"])), width=6)
        ], className="tab-row")
    ]
    return html.Div(content)