import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as p
import plotly.graph_objects as g
import yfinance as y
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(
            id="stock-graph",
            config={
                "displayModeBar": False,
                "displaylogo": False,
                "scrollZoom": False,
                "showTips": False,
            },
            style={
                "height": "180px",
            },
        ),
        dcc.Interval(
            id="interval-component",
            interval=3 * 60 * 1000,
            n_intervals=0,
        ),
    ],
    style={
        "width": "100%",
        "height": "100%",
        "margin": "0",
        "padding": "0",
    },
)


@app.callback(
    Output("stock-graph", "figure"), Input("interval-component", "n_intervals")
)
def update_graph(n):

    stock = y.download("^TWII", period="1d", interval="1m")
    print(stock)

    data = stock.reset_index()
    data.columns = [
        "現在時間",
        "開盤價",
        "最高價",
        "最低價",
        "收盤價",
        "調整後收盤價",
        "成交量",
    ]
    data["現在時間"] = p.to_datetime(data["現在時間"].dt.strftime("%Y-%m-%d %H:%M"))

    fig = g.Figure()

    fig.add_trace(
        g.Scatter(
            name="收盤價",
            x=data["現在時間"],
            y=data["收盤價"],
            mode="lines",
            line=dict(color="#FF7F50"),
        )
    )

    fig.add_shape(
        type="line",
        x0=data["現在時間"].min(),
        x1=data["現在時間"].max(),
        y0=data["收盤價"].mean(),
        y1=data["收盤價"].mean(),
        line=dict(color="red", width=2, dash="dash"),
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis=dict(
            title="時間",
            range=[
                data["現在時間"].min().replace(hour=9, minute=0, second=0),
                data["現在時間"].max().replace(hour=13, minute=30, second=0),
            ],
            dtick=60 * 60 * 1000,  # Hourly ticks
            tickformat="%H",  # Display only hours on x-axis labels
            showgrid=True,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="lightgray",
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis_gridcolor="lightgray",
        yaxis_gridcolor="lightgray",
        margin=dict(l=0, r=0, t=0, b=0),
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="lightgray",
        gridwidth=1,
        tickformat="%H",  # Display only hours on x-axis labels
    )

    fig.update_yaxes(
        showticklabels=False,
        showgrid=True,
        gridcolor="lightgray",
        gridwidth=1,
    )

    fig.update_traces(
        hovertemplate="%{x|%Y-%m-%d %H:%M}<br>收盤價: %{y}<extra></extra>"  # Hover info with hours and minutes
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=False)
