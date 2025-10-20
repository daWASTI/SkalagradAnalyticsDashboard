import statsmodels.api as sm
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px
from typing import Callable, Any

def custom_lowess(df: pd.DataFrame, x_column: str, y_column: str, agg_func: Callable[[pd.Series], Any] = pd.Series.mean, n_exact=0, frac=0.1):
    """
    Returns data for a LOWESS trendline, prepending the first n_exact data points and smoothing the rest
    
    Parameters:
    - x: Pandas Series of the data to be plotted on the x-axis
    - y: Pandas Series of the data to be plotted on the y-axis
    - n_exact: number of points at the start to match exactly
    """

    df_agg = df.groupby(x_column, as_index=False)[y_column].agg(agg_func).reset_index() #aggregate duplicate values in x, since lowess can't handle that

    x = df_agg[x_column]
    y = df_agg[y_column]

    # Compute LOWESS starting after the first n_exact points
    if len(x) > n_exact:
        trend = sm.nonparametric.lowess(
            y[n_exact:], x[n_exact:], frac=frac, it=0, delta=0.0, is_sorted=True
        )
        # Prepend first n_exact points exactly
        trend_x = np.concatenate([x[:n_exact], trend[:,0]])
        trend_y = np.concatenate([y[:n_exact], trend[:,1]])
    else:
        # If fewer points than n_exact, just use the raw data
        trend_x = x
        trend_y = y
    return trend_x, trend_y