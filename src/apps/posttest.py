import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from app import app
from apps import config, posttest, commonmodules
import pandas as pd

#Layout for posttest page
layout = html.Div([
    commonmodules.get_menu(),
    html.H3('IAP measurement Plot'), 
    dcc.Graph(id='graph'),
    html.Div(id='intermediate-value', style={'display': 'none'}),
    html.Div(id='IAP-output'),
])
#produces graph
@app.callback(Output('graph', 'figure'), [Input('intermediate-value', 'children')])
def post_graph(value):
    
    df = pd.read_csv('/home/pi/app/data/' + config.filename + '.csv')
    X = df.iloc[:, 0].tolist()
    Y = df.iloc[:, 1].tolist()

    trace = plotly.graph_objs.Scatter(
        x=X,
        y=Y,
        name='Scatter',
        mode='lines+markers'
    )

    return {'data': [trace],
            'layout': go.Layout(
                height = 550,
                xaxis=dict(range=[min(X), max(X)], title = df.columns[0]),
                yaxis=dict(range=[min(Y), max(Y)], title = df.columns[1])),                   
            }
#produces IAP value at bottom of the page
@app.callback(Output('IAP-output', 'children'),
              [Input('intermediate-value', 'children')])
def display_value_1(value):
    df = pd.read_csv('/home/pi/app/data/' + config.filename + '.csv')
    Y = df.iloc[:, 1].tolist()
    IAP = sum(Y)/len(Y)
    return html.Div([
        html.H4('IAP value of {:.2f} mmHg, gender is {}'.format(IAP, df.columns[2]), style={'textAlign': 'center'})
    ])
