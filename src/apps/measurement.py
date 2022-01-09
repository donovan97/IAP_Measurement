import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from app import app
from apps import database, commonmodules, measurement, home, config, measurement_PT, measurement_PV, measurement_VT
import time
import csv

#Produces the layout for IAP measurement page
layout = html.Div([
    commonmodules.get_menu(),   
    html.H3('Real-time IAP measurement'), 
    html.P('Please select what data to collect and display live:'),
    dcc.Dropdown(
        id='graph-type',
        options=[
            {'label': 'Pressure-Volume', 'value': 'PV'},
            {'label': 'Pressure-Time', 'value': 'PT'},
            {'label': 'Volume-Time', 'value': 'VT'}
        ],
        value='PT',
        style={'width': '45%', 'display': 'inline-block', 'vertical-align': 'middle'}
    ),
    html.P(html.Br()),
    html.P("Please enter the patient's gender:"),
    dcc.Dropdown(
        id='gender-select',
        options=[
            {'label': 'Male', 'value': 'M'},
            {'label': 'Female', 'value': 'F'},
        ],
        value='M',
        style={'width': '45%', 'display': 'inline-block', 'vertical-align': 'middle'}
    ),
    html.P(html.Br()),
    html.P('Please enter a filename to save the data and click start when you wish to begin the test'),
    dcc.Input(id='input-box', type='text',style={'width': '20%', 'display': 'inline-block'}),
    html.Button('Start', id='button', style={'width': '10%', 'display': 'inline-block'}),
    html.Div(id='page-1-content'),
])

#Click start button to start plotting the selected graph type from the dropdown menu. Calls the appropriate function to plot graph
@app.callback(
    dash.dependencies.Output('page-1-content', 'children'),
    [dash.dependencies.Input('button', 'n_clicks'),
    dash.dependencies.Input('graph-type', 'value'),
    dash.dependencies.Input('gender-select', 'value'),
    dash.dependencies.Input('input-box', 'value')])
def update_output(n_clicks, gtype, sex, name):
    if(n_clicks == 1):
        config.X = []
        config.Y = []
        config.time1 = time.time()
        config.filename = name
        if (gtype == "PT"):
            with open('/home/pi/app/data/' + config.filename + '.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Time (s)", "Pressure (mmHg)", sex])
            return measurement_PT.layout
        elif (gtype == "PV"):
            with open('/home/pi/app/data/' + config.filename + '.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Pressure (mmHg)", "Volume (cm^3)", sex])
            return measurement_PV.layout
        elif (gtype == "VT"):
            with open('/home/pi/app/data/' + config.filename + '.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Time (s)", "Distance (mm)", sex])
            return measurement_VT.layout
