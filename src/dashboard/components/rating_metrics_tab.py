import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
import src.dashboard.style as style
import pandas as pd
from src.dashboard.components.figures.plot_helpers import custom_lowess
from typing import Dict
import statsmodels.api as sm
import plotly.graph_objects as go
import numpy as np

#render figures

def render_rating_convergence(rating_convergence_data: pd.DataFrame):
    """
    Plots rating_change vs match_number with a LOWESS trendline.
    The first `n_exact` points are matched exactly, the rest is smoothed.
    
    Parameters:
    - rating_convergence_data: DataFrame with 'match_number' and 'rating_change'
    - n_exact: number of points at the start to match exactly
    """

    trend_x, trend_y = custom_lowess(rating_convergence_data, "match_number", "rating_change", n_exact=4, frac=0.05)

    fig = px.line()
    
    # Create scatter plot
    fig = px.scatter(
        rating_convergence_data,
        x="match_number",
        y="rating_change",
        template="skalagrad_theme",
        title="Rating convergence"
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

    # Apply watermark
    fig = style.add_watermark(fig)

    return fig

def render_rating_convergence_2(rating_convergence_data: pd.DataFrame):
    """
    Plots rating_change vs match_number with a LOWESS trendline.
    The first `n_exact` points are matched exactly, the rest is smoothed.
    
    Parameters:
    - rating_convergence_data: DataFrame with 'match_number' and 'rating_change'
    - n_exact: number of points at the start to match exactly
    """

    trend_x, trend_y = custom_lowess(rating_convergence_data, "match_number", "rating_change", n_exact=4, frac=0.05)

    fig = px.line(
        x=trend_x,
        y=trend_y,
        title="Rating convergence trend"
    )

    fig.update_layout(
        xaxis=dict(range=[-100,2500]),
        yaxis=dict(range=[0,30])
    )

    fig.update_traces(line=dict(color='red', width=3))

    # Apply watermark
    fig = style.add_watermark(fig)

    return fig

#assemble tab

def render(data: Dict[str, pd.DataFrame]):
    content=[
        dbc.Row([
            dbc.Col(dcc.Graph(id="rating1", figure=render_rating_convergence(data["rating_convergence"])), width=6),
            dbc.Col(dcc.Graph(id="rating2", figure=render_rating_convergence_2(data["rating_convergence"])), width=6)
        ], className="tab-row")
    ]
    return html.Div(content)