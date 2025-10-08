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

#load data

def get_daily_matches(engine):
    # Load data
    df = pd.read_sql_query("SELECT matchID, datetime, region FROM MatchData", engine)
    
    # Ensure datetime is a datetime object
    df["datetime"] = pd.to_datetime(df["datetime"])
    
    # Fix missing or 'n/a' regions **in place**
    df["region"] = df["region"].fillna("EU")
    df["region"] = df["region"].replace('"n/a"', "EU")
    
    # Aggregate per day **and keep region**
    daily_counts = (
        df.groupby([df["datetime"].dt.date, "region"])
          .agg(match_count=("matchID", "count"))
          .reset_index()
    )
    
    # Rename for clarity
    daily_counts.rename(columns={"datetime": "date"}, inplace=True)
    return daily_counts

def get_user_count(engine):
    df = pd.read_sql_query(
        "SELECT matchID, userID, datetime FROM PlayerMatchHistory WHERE matchID > 700", 
        engine
    )

    # Ensure datetime is datetime type
    df['datetime'] = pd.to_datetime(df['datetime'])
    df["date"] = df["datetime"].dt.date

    # Aggregate to daily level (unique players per day)
    user_count = (
        df.groupby('date')['userID']
        .apply(set)
        .reset_index(name='players')
        .sort_values('date')
    )

    players_1d, players_7d, players_30d = [], [], []
    cumulative_users = set()
    total_users = []

    for i in range(len(user_count)):
        # 1d
        window_sets = user_count['players'].iloc[max(0, i):i+1]
        players_1d.append(len(set().union(*window_sets)))

        # 7d
        window_sets = user_count['players'].iloc[max(0, i-6):i+1]
        players_7d.append(len(set().union(*window_sets)))

        # 30d
        window_sets = user_count['players'].iloc[max(0, i-29):i+1]
        players_30d.append(len(set().union(*window_sets)))

        # cumulative total users
        cumulative_users |= user_count['players'].iloc[i]
        total_users.append(len(cumulative_users))

    user_count['players_1d'] = players_1d
    user_count['players_7d'] = players_7d
    user_count['players_30d'] = players_30d
    user_count['total_users'] = total_users

    return user_count


def get_rating_convergence(engine):
    df = pd.read_sql_query("SELECT matchID, userID, dMMR FROM PlayerMatchHistory", engine)
    df["dMMR"] = abs(df["dMMR"])
    df.rename(columns={"dMMR":"rating_change"}, inplace=True)
    df.sort_values(by=["userID", "matchID"])
    df["match_number"] = df.groupby("userID").cumcount() + 1
    rating_convergence = df.groupby("match_number")["rating_change"].mean().reset_index()
    return rating_convergence

def get_matchmaking_convergence(engine):
    df = pd.read_sql_query("SELECT match_id, user_id, team_score_ratio FROM PlayerMatchHistoryCleaned", engine)
    # Ensure team_score_ratio is numeric
    df['team_score_ratio'] = df['team_score_ratio'].astype(float)
    # Sort by user and matchID
    df = df.sort_values(by=['user_id', 'match_id'])
    # Compute each player's match number (1-based)
    df['match_number'] = df.groupby('user_id').cumcount() + 1
    # Aggregate team_score_ratio by match_number across all players
    matchmaking_convergence = df.groupby('match_number')['team_score_ratio'].mean().reset_index()
    return matchmaking_convergence

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

def render_rating_convergence(rating_convergence_data: pd.DataFrame, n_exact=4):
    """
    Plots rating_change vs match_number with a LOWESS trendline.
    The first `n_exact` points are matched exactly, the rest is smoothed.
    
    Parameters:
    - rating_convergence_data: DataFrame with 'match_number' and 'rating_change'
    - n_exact: number of points at the start to match exactly
    """

    x = rating_convergence_data['match_number'].values
    y = rating_convergence_data['rating_change'].values

    # Compute LOWESS starting after the first n_exact points
    if len(x) > n_exact:
        trend = sm.nonparametric.lowess(
            y[n_exact:], x[n_exact:], frac=0.05, it=0, delta=0.0, is_sorted=True
        )
        # Prepend first n_exact points exactly
        trend_x = np.concatenate([x[:n_exact], trend[:,0]])
        trend_y = np.concatenate([y[:n_exact], trend[:,1]])
    else:
        # If fewer points than n_exact, just use the raw data
        trend_x = x
        trend_y = y

    # Create scatter plot
    fig = px.scatter(
        rating_convergence_data,
        x="match_number",
        y="rating_change",
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

def render(engine):
    daily_matches_data = get_daily_matches(engine)
    rating_convergence_data = get_rating_convergence(engine).iloc[1:500]
    matchmaking_convergence_data = get_matchmaking_convergence(engine)
    user_count_data = get_user_count(engine)
    content=[
        dbc.Row([
            dbc.Col(dcc.Graph(id="overview1", figure=render_daily_matches(daily_matches_data)), width=6),
            dbc.Col(dcc.Graph(id="overview1", figure=render_user_count(user_count_data)), width=6)
        ], className="tab-row"),
        dbc.Row([
            dbc.Col(dcc.Graph(id="overview2", figure=render_rating_convergence(rating_convergence_data)), width=6),
            dbc.Col(dcc.Graph(id="overview3", figure=render_matchmaking_convergence(matchmaking_convergence_data)), width=6)
        ], className="tab-row")
    ]
    return html.Div(content)