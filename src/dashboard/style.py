import plotly.io as pio
import plotly.express as px
import seaborn as sns
import base64
import os

#base colors
PLAYER_COLORS = ["#1f2c56", "#2a3f5f", "#ff7f0e", "#2ca02c"]
TEAM_COLORS = ["#d62728", "#9467bd", "#8c564b"]
SCORE_COLORS = ["#bfa97c", "#e377c2"]
SKALA_MAIN_COLORS = ["#0d1019", "#bfa97c", "#1b1c1e", "#ee7600"]
SKALA_BLUE = "#0d1019"
SKALA_GREY = "#1b1c1e"
SKALA_YELLOW = "#bfa97c"
SKALA_ORANGE = "#ee7600"
BG_COLOR = "#e6d8bc"
PLOT_BG_COLOR = "#797a6d"

def add_watermark(fig, logo_path="/assets/SkalaWatermark.png", opacity=0.7, size=0.3):
    fig.add_layout_image(
        dict(
            source=logo_path,
            xref="paper", yref="paper",
            x=0.8, y=0.9,
            xanchor="center", yanchor="middle",
            sizex=size, sizey=size,
            opacity=opacity,
            layer="above"
        )
    )
    return fig

#color palettes
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))

def get_blend_palette(colors=[SKALA_YELLOW, SKALA_ORANGE]):
    return [rgb_to_hex(c) for c in sns.blend_palette(colors, n_colors=7, as_cmap=False)]

#Custom Skalagrad theme
skalagrad_theme = dict(
    layout= dict(
        font=dict(family="Arial", size=14, color="#0d1019"),
        title=dict(font=dict(size=20, color="#0d1019")),
        paper_bgcolor= BG_COLOR,
        plot_bgcolor=PLOT_BG_COLOR,
        xaxis=dict(showgrid=True, gridcolor="#535353", zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#585858", zeroline=False),
        legend=dict(title_font=dict(size=14), font=dict(size=12))
    ),
    data=dict(
        scatter=[dict(marker=dict(size=10, line=dict(width=1, color="#c7af2b")))],
        bar=[dict(marker=dict(color="#f0bd31", line=dict(width=0.5, color="#dfbf30")))]
    )
)

#Register theme
def init():
    pio.templates["skalagrad_theme"] = skalagrad_theme
    pio.templates.default = "skalagrad_theme"