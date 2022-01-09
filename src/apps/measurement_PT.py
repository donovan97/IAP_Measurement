import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from pressure import pressure
from app import app
from apps import config, posttest, commonmodules
import time
import csv

#Produces layout for PT measurement
layout = html.Div([
    dcc.Graph(id='live-graph-PT',
                animate=False,),
    dcc.Interval(
        id='graph-update-PT',
        interval=0.6*1000
    ),
    dcc.Link('Stop', href='/posttest', className="button"),
])

#Produces graph for PT measurement
@app.callback(Output('live-graph-PT', 'figure'),
              [Input('graph-update-PT', 'n_intervals')])
def update_graph_PT(n):
    pressure_meas = pressure()
    config.time2 = time.time()
    time_interval = config.time2 - config.time1
    config.X.append(time_interval)
    config.Y.append(pressure_meas)

    with open('/home/pi/app/data/' + config.filename + '.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([time_interval, pressure_meas])

    trace = plotly.graph_objs.Scatter(
        x=config.X,
        y=config.Y,
        name='Scatter',
        mode='lines+markers'
    )

    return {'data': [trace],
            'layout': go.Layout(
                height=600,
                xaxis=dict(range=[min(config.X), max(config.X)], title = 'Time (s)'),
                yaxis=dict(range=[min(config.Y), max(config.Y)], title = 'Pressure (mmHg)')),
            }
