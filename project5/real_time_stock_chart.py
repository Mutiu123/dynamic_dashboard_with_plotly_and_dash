import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc, Output, Input, State

app = Dash(__name__)

# ---------- LAYOUT ----------
app.layout = html.Div(
    style={'backgroundColor': '#111111', 'color': '#FFFFFF', 'padding': '20px'},
    children=[
        html.H1(
            "Stock Candlestick Chart Tool",
            style={'textAlign': 'center', 'color': '#FFFFFF'}
        ),

        html.Div([
            html.Label("Enter Stock Ticker", style={'color': '#FFFFFF'}),
            dcc.Input(
                id='ticker-input',
                type='text',
                value='AAPL',
                style={'backgroundColor': '#333333', 'color': '#FFFFFF'}
            )
        ], style={'padding': '10px'}),

        html.Div([
            html.Label("Select Start Date", style={'color': '#FFFFFF'}),
            dcc.DatePickerSingle(id='start-date-picker', date='2023-01-01')
        ], style={'padding': '10px'}),

        html.Div([
            html.Label("Select End Date", style={'color': '#FFFFFF'}),
            dcc.DatePickerSingle(id='end-date-picker', date='2025-01-01')
        ], style={'padding': '10px'}),

        html.Div([
            html.Button(
                'Submit',
                id='submit-button',
                n_clicks=0,
                style={'backgroundColor': '#444444', 'color': '#FFFFFF'}
            )
        ], style={'padding': '10px', 'textAlign': 'center'}),

        html.Div(
            id='chart-container',
            style={'visibility': 'hidden'},
            children=[
                dcc.Graph(
                    id='candlestick-chart',
                    style={'backgroundColor': '#111111'}
                )
            ]
        )
    ]
)

# ---------- CALLBACK ----------
@app.callback(
    Output('candlestick-chart', 'figure'),
    Output('chart-container', 'style'),
    Input('submit-button', 'n_clicks'),
    State('ticker-input', 'value'),
    State('start-date-picker', 'date'),
    State('end-date-picker', 'date'),
)
def update_chart(n_clicks, ticker, start_date, end_date):
    # initial page load: don't show anything
    if not n_clicks:
        return go.Figure(), {'visibility': 'hidden'}

    # download price data
    df = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        group_by="column"
    )

    print("Downloaded rows:", len(df))
    print("Original columns:", df.columns)

    if df.empty:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="No data returned for this ticker/date range",
            template="plotly_dark",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
        )
        return empty_fig, {'visibility': 'visible'}

    # If columns are MultiIndex like ('Open','AAPL'), drop the ticker level
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
        print("Simplified columns:", df.columns)

    # ensure required columns exist
    for col in ['Open', 'High', 'Low', 'Close']:
        if col not in df.columns:
            fig = go.Figure()
            fig.update_layout(
                title=f"Missing '{col}' data for {ticker}",
                template="plotly_dark",
                xaxis_title="Date",
                yaxis_title="Price (USD)",
            )
            return fig, {'visibility': 'visible'}

    # put the index into a Date column
    df = df.reset_index()
    df['Date'] = pd.to_datetime(df['Date'])

    # build candlestick figure
    fig = go.Figure()
    fig.add_trace(
        go.Candlestick(
            x=df['Date'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name=ticker
        )
    )

    fig.update_layout(
        title=f'Candlestick Chart of {ticker}',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        xaxis_rangeslider_visible=False,
        template='plotly_dark'
    )

    return fig, {'visibility': 'visible'}

# ---------- MAIN ----------
if __name__ == '__main__':
    app.run(debug=True)
