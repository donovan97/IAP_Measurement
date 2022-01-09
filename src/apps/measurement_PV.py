import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from distance import distance
from pressure import pressure
from app import app
from apps import config, posttest, commonmodules
import time
import csv

#Produces layout for PV measurement
layout = html.Div([
    dcc.Graph(id='live-graph-PV',
                animate=False,),
    dcc.Interval(
        id='graph-update-PV',
        interval=0.6*1000
    ),
    dcc.Link('Stop', href='/posttest', className="button"),
])

#Callback for PV measurement
@app.callback(Output('live-graph-PV', 'figure'),
              [Input('graph-update-PV', 'n_intervals')])
def update_graph_PV(n):
    pressure_meas = pressure()
    volume_meas = distance()
    config.X.append(pressure_meas)
    config.Y.append(volume_meas)

    with open('/home/pi/app/data/' + config.filename + '.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([pressure_meas, volume_meas])

    trace = plotly.graph_objs.Scatter(
        x=config.X,
        y=config.Y,
        name='Scatter',
        mode='lines+markers'
    )

    return {'data': [trace],
            'layout': go.Layout(
                height=600,
                xaxis=dict(range=[min(config.X), max(config.X)], title = 'Volume (cm^3)'),
                yaxis=dict(range=[min(config.Y), max(config.Y)], title = 'Pressure (mmHg)')),
            }
