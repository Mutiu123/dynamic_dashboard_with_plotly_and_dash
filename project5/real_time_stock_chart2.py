"""
Stock Candlestick Dashboard
--------------------------------------------
This Dash application retrieves stock price data using yfinance
and displays an interactive candlestick chart. Users can select:
    • Stock ticker symbol
    • Start date
    • End date
    • Submit button triggers chart update

The layout is a full-screen, two-column design:
    • Left column: input controls
    • Right column: candlestick chart
"""

import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc, Output, Input, State

# ------------------------------------------------------------
# Initialize Dash App
# ------------------------------------------------------------
app = Dash(__name__)

# ------------------------------------------------------------
# App Layout (Full Screen Responsive Design)
# ------------------------------------------------------------
app.layout = html.Div(
    style={
        'backgroundColor': '#111111',
        'color': '#FFFFFF',
        'height': '100vh',           # full viewport height
        'width': '100vw',            # full viewport width
        'margin': '0',
        'padding': '0',
        'overflow': 'hidden'
    },
    children=[

        # ---------------------- Page Title ----------------------
        html.H1(
            "Stock Candlestick Chart Tool",
            style={
                'textAlign': 'center',
                'color': '#FFFFFF',
                'marginTop': '10px',
                'marginBottom': '30px',
                'fontSize': '36px'
            }
        ),

        # --------------------------------------------------------
        # Main Flex Container (Left controls + Right chart)
        # --------------------------------------------------------
        html.Div(
            style={
                'display': 'flex',
                'flexDirection': 'row',
                'height': '90%',              # take remaining screen height
                'paddingLeft': '20px'
            },
            children=[

                # ------------------ Left Control Panel ------------------
                html.Div(
                    style={
                        'width': '300px',
                        'padding': '10px',
                        'paddingRight': '30px'
                    },
                    children=[

                        # --- Stock Ticker Input ---
                        html.Div([
                            html.Label("Enter Stock Ticker"),
                            dcc.Input(
                                id='ticker-input',
                                type='text',
                                value='AAPL',
                                placeholder='e.g. AAPL, MSFT, TSLA',
                                style={
                                    'backgroundColor': '#333333',
                                    'color': '#FFFFFF',
                                    'width': '100%',
                                    'padding': '8px'
                                }
                            )
                        ], style={'marginBottom': '20px'}),

                        # --- Start Date Picker ---
                        html.Div([
                            html.Label("Select Start Date"),
                            dcc.DatePickerSingle(
                                id='start-date-picker',
                                date='2025-01-01'
                            )
                        ], style={'marginBottom': '20px'}),

                        # --- End Date Picker ---
                        html.Div([
                            html.Label("Select End Date"),
                            dcc.DatePickerSingle(
                                id='end-date-picker',
                                date='2025-05-15'
                            )
                        ], style={'marginBottom': '20px'}),

                        # --- Submit Button ---
                        html.Button(
                            "Submit",
                            id='submit-button',
                            n_clicks=0,
                            style={
                                'backgroundColor': '#444444',
                                'color': '#FFFFFF',
                                'padding': '10px 25px',
                                'border': 'none',
                                'cursor': 'pointer',
                                'fontSize': '16px'
                            }
                        )
                    ]
                ),

                # ------------------ Right Chart Area ------------------
                html.Div(
                    id='chart-container',
                    style={
                        'flex': 1,
                        'visibility': 'hidden',    # hidden until user clicks Submit
                        'paddingRight': '20px'
                    },
                    children=[
                        dcc.Graph(
                            id='candlestick-chart',
                            style={
                                'height': '100%',
                                'width': '100%',
                                'backgroundColor': '#111111'
                            }
                        )
                    ]
                )
            ]
        )
    ]
)

# ------------------------------------------------------------
# Callback: Fetch Data + Build Candlestick Chart
# ------------------------------------------------------------
@app.callback(
    Output('candlestick-chart', 'figure'),
    Output('chart-container', 'style'),
    Input('submit-button', 'n_clicks'),
    State('ticker-input', 'value'),
    State('start-date-picker', 'date'),
    State('end-date-picker', 'date')
)
def update_chart(n_clicks, ticker, start_date, end_date):
    """
    When the user clicks Submit:
        1. Download OHLC stock data from Yahoo Finance
        2. Normalize MultiIndex columns
        3. Build a Plotly candlestick chart
        4. Make the chart visible
    """

    # Before first click → keep chart hidden
    if not n_clicks:
        return go.Figure(), {'flex': 1, 'visibility': 'hidden'}

    # ------------------- Download OHLC Data -------------------
    df = yf.download(ticker, start=start_date, end=end_date, group_by="column")

    # Handle empty results (invalid ticker or no data)
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No data returned for this ticker or date range.",
            template="plotly_dark"
        )
        return fig, {'flex': 1, 'visibility': 'visible'}

    # Convert MultiIndex columns to single-level: "Open", "High", etc.
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Validate required OHLC fields
    required_cols = ['Open', 'High', 'Low', 'Close']
    for col in required_cols:
        if col not in df.columns:
            fig = go.Figure()
            fig.update_layout(
                title=f"Missing '{col}' data for {ticker}.",
                template="plotly_dark"
            )
            return fig, {'flex': 1, 'visibility': 'visible'}

    # Reset index so Date becomes a regular column
    df = df.reset_index()

    # ------------------- Build Candlestick Chart -------------------
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name=ticker.upper()
            )
        ]
    )

    # Apply chart styling
    fig.update_layout(
        title=f"Candlestick Chart of {ticker.upper()}",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=False,
        template="plotly_dark"
    )

    return fig, {'flex': 1, 'visibility': 'visible'}


# ------------------------------------------------------------
# Run Application
# ------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
