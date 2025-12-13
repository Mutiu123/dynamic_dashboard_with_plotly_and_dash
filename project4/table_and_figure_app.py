
"""
# code to feched califonial housing dataset
from sklearn.datasets import fetch_california_housing
df = fetch_california_housing(as_frame=True).frame 
df.to_csv('housing2.csv', index=None) 
""" 

import pandas as pd
import plotly.express as px 
from dash import Dash, html, dash_table, dcc, callback, Output, Input 

df = pd.read_csv('housing2.csv') 

app = Dash() 

app.layout = [ 
              html.Div(children='Dashboard'),
              dash_table.DataTable(data=df.to_dict('records'), page_size=7),
              html.Div([
                  html.Label('Select Feature:'),
                  dcc.Dropdown(
                      id='feature-dropdown',
                      options=[{'label': col, 'value': col} for col in df.columns],
                      value=df.columns[0]
                  )
              ]),
              dcc.Graph(id='histogram')
                           
]
@app.callback(
    Output(component_id='histogram', component_property='figure'),
    Input(component_id= 'feature-dropdown', component_property= 'value')
    )

def update_histogram(selected_feature):
    fig = px.histogram(df, x=selected_feature)
    fig.update_layout(title=f'Histogram of {selected_feature}',
                      xaxis_title=selected_feature,
                      yaxis_title='Frequency')

    return fig

if __name__=='__main__':
    app.run(debug=True)