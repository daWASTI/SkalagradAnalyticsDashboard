import dash_bootstrap_components as dbc

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
        #styling
        style={
            "padding": "10px",
        }
    )