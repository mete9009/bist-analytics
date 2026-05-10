import plotly.graph_objects as go
from plotly.subplots import make_subplots

_CARD    = "#111827"
_BORDER  = "#1a2540"
_TEXT    = "#64748b"
_TEXT1   = "#94a3b8"

def _base_layout(**kw):
    cfg = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=_CARD,
        font=dict(family="Inter, sans-serif", color=_TEXT, size=11),
        xaxis=dict(gridcolor=_BORDER, linecolor=_BORDER, tickfont=dict(color=_TEXT), zeroline=False),
        yaxis=dict(gridcolor=_BORDER, linecolor=_BORDER, tickfont=dict(color=_TEXT), zeroline=False),
        margin=dict(l=8, r=8, t=8, b=8),
        legend=dict(font=dict(color=_TEXT1, size=11), bgcolor="rgba(0,0,0,0)"),
        xaxis_rangeslider_visible=False,
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#1e293b", bordercolor=_BORDER, font=dict(color="#f1f5f9")),
    )
    cfg.update(kw)
    return cfg

def create_candlestick(df):
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        row_heights=[0.72, 0.28], vertical_spacing=0.02
    )

    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["Open"], high=df["High"],
        low=df["Low"],   close=df["Close"],
        name="Fiyat",
        increasing=dict(line=dict(color="#10b981"), fillcolor="#10b981"),
        decreasing=dict(line=dict(color="#ef4444"), fillcolor="#ef4444"),
    ), row=1, col=1)

    colors = [
        "#10b981" if c >= o else "#ef4444"
        for c, o in zip(df["Close"], df["Open"])
    ]
    fig.add_trace(go.Bar(
        x=df.index, y=df["Volume"],
        name="Hacim",
        marker_color=colors,
        opacity=0.5,
    ), row=2, col=1)

    layout = _base_layout(height=500)
    layout["yaxis2"] = dict(gridcolor=_BORDER, linecolor=_BORDER, tickfont=dict(color=_TEXT), zeroline=False)
    layout["legend"] = dict(
        orientation="h",
        x=0, y=1.04,
        xanchor="left", yanchor="bottom",
        font=dict(color=_TEXT1, size=11),
        bgcolor="rgba(0,0,0,0)",
    )
    layout["margin"] = dict(l=8, r=8, t=44, b=8)
    fig.update_layout(**layout)
    fig.update_xaxes(rangeslider_visible=False)
    return fig
