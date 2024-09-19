import dash
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    stock_code = pathname.strip("/").upper()
    if not stock_code or stock_code == "0":
        stock_code = "^TWII"
    graph_style = {
        "height": "180px" if stock_code == "^TWII" else "400px",
        "width": "100%",
    }

    return html.Div(
        [
            dcc.Graph(
                id="stock-graph",
                config={
                    "displayModeBar": False,
                    "displaylogo": False,
                    "scrollZoom": False,
                    "showTips": True,
                    "staticPlot": False,
                },
                style=graph_style,
            ),
        ],
        style={
            "width": "100%",
            "height": "400px",
            "margin": "0",
            "padding": "0",
        },
    )


@app.callback(Output("stock-graph", "figure"), Input("url", "pathname"))
def update_graph(pathname):
    stock_codes = pathname.strip("/").upper().split(",")
    if not stock_codes or stock_codes[0] == "" or "0" in stock_codes:
        stock_codes = ["^TWII"]

    fig = go.Figure()
    for stock_code in stock_codes:
        stock_code_full = f"{stock_code}.TW" if stock_code != "^TWII" else "^TWII"

        try:
            stock_data = yf.download(stock_code_full, period="1d", interval="1m")
            if stock_data.empty:
                continue

            data = stock_data.reset_index()
            data.columns = [
                "現在時間",
                "開盤價",
                "最高價",
                "最低價",
                "收盤價",
                "調整後收盤價",
                "成交量",
            ]
            data["現在時間"] = pd.to_datetime(
                data["現在時間"].dt.strftime("%Y-%m-%d %H:%M")
            )

            fig.add_trace(
                go.Scatter(
                    name=f"股價 ({stock_code_full})",
                    x=data["現在時間"],
                    y=data["收盤價"],
                    mode="lines",
                    line=dict(color="#FF7F50"),
                    hovertemplate=(
                        "時間: %{x|%Y-%m-%d %H:%M}<br>股價: %{y}<extra></extra>"
                    ),
                )
            )

            if stock_code != "^TWII":
                data["成交量"] //= 1000
                fig.add_trace(
                    go.Bar(
                        name=f"成交量 ({stock_code_full})",
                        x=data["現在時間"],
                        y=data["成交量"],
                        yaxis="y2",
                        marker_color="#99ccff",
                        hovertemplate=("成交量: %{y} 張<extra></extra>"),
                    )
                )

        except Exception as e:
            print(f"更新圖表時發生錯誤 ({stock_code_full}): {e}")

    min_price = (
        min(
            [trace.y.min() for trace in fig.data if isinstance(trace, go.Scatter)],
            default=0,
        )
        - 50
    )
    max_price = (
        max(
            [trace.y.max() for trace in fig.data if isinstance(trace, go.Scatter)],
            default=100,
        )
        + 50
    )
    tick_interval = 10

    if "^TWII" in stock_codes:
        fig.update_layout(
            hovermode="x unified",
            xaxis=dict(
                title="時間",
                range=[
                    data["現在時間"].min().replace(hour=9, minute=0, second=0),
                    data["現在時間"].max().replace(hour=13, minute=30, second=0),
                ],
                dtick=60 * 60 * 1000,
                tickformat="%H",
                showgrid=True,
                showticklabels=True,
                fixedrange=True,
            ),
            yaxis=dict(
                title="",
                showticklabels=False,
                showgrid=False,
                fixedrange=True,
            ),
            yaxis2=dict(
                title="",
                overlaying="y",
                side="right",
                visible=False,
                fixedrange=True,
                showgrid=False,
            ),
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis_gridcolor="lightgray",
            margin=dict(l=0, r=0, t=0, b=0),
        )
    else:
        fig.update_layout(
            hovermode="x unified",
            xaxis=dict(
                title="時間",
                range=[
                    data["現在時間"].min().replace(hour=9, minute=0, second=0),
                    data["現在時間"].max().replace(hour=13, minute=30, second=0),
                ],
                dtick=60 * 60 * 1000,
                tickformat="%H:%M",
                showgrid=True,
                showticklabels=True,
                fixedrange=True,
            ),
            yaxis=dict(
                title="股價",
                range=[min_price, max_price],
                dtick=tick_interval,
                automargin=True,
                fixedrange=True,
                showgrid=True,
                showline=True,
                showticklabels=True,
                linecolor="#000",
                linewidth=1,
                ticks="outside",
            ),
            yaxis2=dict(
                title="成交量（張）",
                overlaying="y",
                side="right",
                visible=True,
                automargin=True,
                fixedrange=True,
                showgrid=False,
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
    )

    fig.update_yaxes(
        showticklabels=True,
        showgrid=True,
        gridcolor="lightgray",
        gridwidth=1,
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=False)


def calculate_percentage_change(data):

    first_close = data["收盤價"].iloc[0]
    last_close = data["收盤價"].iloc[-1]
    percent_change = ((last_close - first_close) / first_close) * 100
    return percent_change


def get_stock_data(stock_code):
    stock_code_full = f"{stock_code}.TW" if stock_code != "^TWII" else "^TWII"

    try:
        stock_data = yf.download(stock_code_full, period="1d", interval="1m")
        if stock_data.empty:
            return None, None, None  # 返回三個 None

        data = stock_data.reset_index()
        data.columns = [
            "現在時間",
            "開盤價",
            "最高價",
            "最低價",
            "收盤價",
            "調整後收盤價",
            "成交量",
        ]
        data["現在時間"] = pd.to_datetime(
            data["現在時間"].dt.strftime("%Y-%m-%d %H:%M")
        )

        latest_price = data["收盤價"].iloc[-1]
        opening_price = data["開盤價"].iloc[0]  # 獲取開盤價格

        percent_change = calculate_percentage_change(data)
        price_change = latest_price - opening_price  # 計算漲跌（元）
        total_volume = data["成交量"].sum()  # 總成交量
        trading_units = total_volume // 100  # 計算成交張數（1 張 = 100 股）

        return latest_price, percent_change, price_change, trading_units  # 返回四個值

    except Exception as e:
        print(f"獲取數據時發生錯誤: {e}")
        return None, None, None, None  # 返回四個 None
