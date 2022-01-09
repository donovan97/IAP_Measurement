import plotly
import plotly.graph_objs as go
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from apps import commonmodules, config
import pandas as pd
from app import app
import glob 
import os

#Layout for database page
layout = html.Div([
    commonmodules.get_menu(),   
    html.H3('IAP measurement database'), 
    html.P('Select measurement to download or delete'),
    dcc.Dropdown(id="dropdown", style={'width': '45%', 'display': 'inline-block', 'vertical-align': 'middle'}),
    dcc.Interval(
        id='page-update',
        interval=0.5*1000
    ),
    html.P(html.Br()),
    html.A('Download CSV', id='my-link', className="button"),
    html.A('Delete file', id='delete-link', className="button", style={'color':'red'}),
    dcc.Graph(id='graph_database'),
    html.Div(id='IAP-output-database'),
])
#Callback for dropdown menu options, needs interval to refresh if ever one is deleted
@app.callback(
    Output('dropdown', 'options'),
    [Input('page-update', 'n_intervals')])
def update_dropdown(value):
    config.filelist = glob.glob("/home/pi/app/data/*.csv")
    return [{'label': i, 'value': i} for i in config.filelist]

#Callback for downloading a CSV
@app.callback(Output('my-link', 'href'), [Input('dropdown', 'value')])
def update_link(value):
    return '/dash/urlToDownload?value={}'.format(value)

#Flask instance for downloading CSV
@app.server.route('/dash/urlToDownload')
def download_csv():
    value = flask.request.args.get('value')
    return flask.send_file(value,
                           mimetype='text/csv',
                           attachment_filename=value,
                           as_attachment=True)

#Callback for deleting file
@app.callback(Output('delete-link', 'href'), [Input('dropdown', 'value')])
def update_link2(value):
    return '/dash/urlToDelete?value={}'.format(value)

#Flask instance for deleting file
@app.server.route('/dash/urlToDelete')
def delete_csv():
    value = flask.request.args.get('value')
    os.remove(value)
    return ('', 204)

#Callback to produce graph
@app.callback(Output('graph_database', 'figure'), [Input('dropdown', 'value')])
def update_graph_scatter(value):
    
    df = pd.read_csv(str(value))
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
                height=550,
                xaxis=dict(range=[min(X), max(X)], title = df.columns[0]),
                yaxis=dict(range=[min(Y), max(Y)], title = df.columns[1])),            
            }

#Callback to calculate and output IAP value
@app.callback(Output('IAP-output-database', 'children'),
              [Input('dropdown', 'value')])
def display_value_2(value):
    if (value == None):
        return
    df2 = pd.read_csv(str(value))
    Y_2 = df2.iloc[:, 1].tolist()
    IAP_2 = sum(Y_2)/len(Y_2)
    return html.Div([
        html.H4('IAP value of {:.2f} mmHg, gender is {}'.format(IAP_2, df2.columns[2]), style={'textAlign': 'center'})
    ])