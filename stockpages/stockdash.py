import argparse
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd


parser = argparse.ArgumentParser(description="Dash 应用展示股票数据")
parser.add_argument("id", type=str, help="股票代码")
args = parser.parse_args()
stock_code = args.id.strip().upper()


app = dash.Dash(__name__)


app.layout = html.Div(
    [
        html.H1(f"股票即時數據 - {stock_code}"),
        dcc.Graph(id="stock-graph"),
        dcc.Link("返回首页", href="/"),
    ]
)


@app.callback(
    Output("stock-graph", "figure"),
    [Input("stock-graph", "id")],
)
def update_graph(_):
    stock_code_full = f"{stock_code}.TW"

    try:
        stock_data = yf.download(stock_code_full, period="1d", interval="1m")
        if stock_data.empty:
            return go.Figure()

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
        data["成交量"] //= 1000

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                name=f"成交量 ({stock_code_full})",
                x=data["現在時間"],
                y=data["成交量"],
                yaxis="y2",
                marker_color="#99ccff",
                hovertext=[
                    f"時間: {x}<br>成交量: {y} 張"
                    for x, y in zip(data["現在時間"], data["成交量"])
                ],
                hoverinfo="text",
            )
        )

        fig.add_trace(
            go.Candlestick(
                name=f"K線圖 ({stock_code_full})",
                x=data["現在時間"],
                open=data["開盤價"],
                high=data["最高價"],
                low=data["最低價"],
                close=data["收盤價"],
                increasing_line_color="#fd5047",
                increasing_fillcolor="#f29696",
                decreasing_line_color="#3d9970",
                decreasing_fillcolor="#91c2b3",
                hovertext=[
                    f"開盤價: {o}<br>最高價: {h}<br>最低價: {l}<br>收盤價: {c}"
                    for x, o, h, l, c in zip(
                        data["現在時間"],
                        data["開盤價"],
                        data["最高價"],
                        data["最低價"],
                        data["收盤價"],
                    )
                ],
                hoverinfo="text",
            )
        )

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
                fixedrange=True,
            ),
            yaxis=dict(
                title="股價",
                dtick=2,
                automargin=True,
            ),
            yaxis2=dict(
                title="成交量（張）",
                overlaying="y",
                side="right",
                visible=True,
                automargin=True,
            ),
        )

        fig.update_xaxes(
            dtick=60 * 60 * 1000,
            tickformat="%H:%M",
            fixedrange=True,
        )

        return fig
    except Exception as e:
        print(f"更新圖表時發生錯誤: {e}")
        return go.Figure()


if __name__ == "__main__":
    app.run_server(debug=True)
