import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
import src.dashboard.style as style
import pandas as pd
from dash_extensions.enrich import DashProxy, Serverside, Trigger
from typing import Dict

#load data
df_players = pd.DataFrame({
    "Player": ["A", "B", "C", "D", "E"],
    "Kills": [10, 23, 15, 7, 19],
    "Assists": [5, 10, 9, 4, 12],
    "Team": ["Red", "Red", "Blue", "Blue", "Blue"],
    "ScoreBias": [5, -5, 1, 0, -2]
})

dummy_data = {"daily_matches":df_players}

def get_daily_matches(engine=None):
    #df = pd.read_sql_query(f"SELECT matchID, datetime FROM MatchData", engine)
    return df_players

def get_cached_data():
    daily_matches = get_daily_matches()
    return Serverside({"daily_matches": daily_matches})

def render(data: Dict[str, pd.DataFrame]):
    df_test = data["daily_matches"]
    content=[
        dbc.Row([
            dbc.Col(dcc.Graph(figure=style.add_watermark(px.bar(df_test, x="Player", y="Kills", color="Player", color_discrete_sequence=style.get_blend_palette([style.SKALA_BLUE, style.SKALA_ORANGE]), template="skalagrad_theme"))), width=6),
            dbc.Col(dcc.Graph(figure=style.add_watermark(px.bar(df_test, x="Player", y="Assists", color="Player", color_discrete_sequence=style.get_blend_palette(), template="skalagrad_theme"))), width=6)
        ], className="tab-row"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=style.add_watermark(px.bar(df_test, x="Player", y="Kills", color="Player", color_discrete_sequence=style.get_blend_palette(), template="skalagrad_theme"))), width=6),
            dbc.Col(dcc.Graph(figure=style.add_watermark(px.bar(df_test, x="Player", y="Assists", color="Player", color_discrete_sequence=style.get_blend_palette(), template="skalagrad_theme"))), width=6)
        ], className="tab-row")
    ]
    return html.Div(content)