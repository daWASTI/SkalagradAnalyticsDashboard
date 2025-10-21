import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.development.base_component import Component
from typing import List, Union
import src.dashboard.style as style
import plotly.express as px
import plotly.graph_objects as go
import uuid

def create_tab(label: str, tab_id: str, children: list):
    """
    Helper function to create a dbc.Tab with consistent styling.

    Parameters
    ----------
    label : str
        The displayed text on the tab button.
    tab_id : str
        Unique identifier for the tab (used for callbacks).
    children : list
        The Dash components (layout) that will appear inside the tab.

    Returns
    -------
    dbc.Tab
        A Dash Bootstrap Component Tab with consistent styling.
    """
    return dbc.Tab(
        label=label,
        tab_id=tab_id,
        children=children,
        style={
            "padding": "10px",
        }
    )

def create_graph(fig: go.Figure, row_id: str) -> dcc.Graph:
    return dcc.Graph(
                id={"type": "graph", "index": row_id},
                figure=fig,
                config={"displayModeBar": False},
                style={
                    "height": "100%",
                    "width": "100%",
                },
            )

def create_graph_column(graph: dcc.Graph) -> dbc.Col:
    return dbc.Col(
                html.Div(
                    graph,
                    style={
                        "height": "100%",
                        "display": "flex",
                        "alignItems": "stretch",
                    },
                ),
                width=6,
                style={"padding": "0"},
            )

def create_markdown_column(markdown: dcc.Markdown) -> dbc.Col:
    return dbc.Col(
                    html.Div(
                        markdown,
                        style={
                            "backgroundColor": style.BG_COLOR,
                            "borderRadius": "0",
                            "padding": "1rem",
                            "height": "100%",
                        },
                    ),
                    width=6,
                    style={"padding": "0"},
                )

def create_row(fig: go.Figure, text: str, order: bool = True, marginTop: str = "0", marginBottom: str = "3rem", delay="0s"):
    row_id = str(uuid.uuid4())
    graph = create_graph(fig, row_id)
    markdown = dcc.Markdown(text, id={"type": "markdown", "index": row_id}, style={"display": "none"})
    graph_col = create_graph_column(graph)
    markdown_col = create_markdown_column(markdown)
    cols = [graph_col, markdown_col] if order else [markdown_col, graph_col]
    row = dbc.Row(cols,
            className="tab-row",
            style={"alignItems": "stretch", "height": "500px", "marginTop": marginTop, "marginBottom": marginBottom},
        )
    animated_row = html.Div(
        row,
        id={"type": "animated-row", "index": row_id},
        style={"animationDelay": delay}
    )
    return dcc.Loading(children=animated_row, type="default", fullscreen=False)