import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from apps import database, measurement, commonmodules
import os
from app import app

#Layout for home page
layout = html.Div([
    commonmodules.get_menu(),
    html.H3('Welcome'),
    html.P('Before taking an IAP measurement, please read the instructions below.'),
    html.Br(),
    html.P('This device is intended to be used to measure intra-abdominal pressure (IAP). [Give instructions for IAP measurement].'),
    html.P('To start a test, navigate to the "IAP measurement" tab, input the required information and click start. To end the test, click stop.'),
    html.P('To view previous tests, download data or delete the test from the device, navigate to the database tab.'),
    html.P('To turn off the device, click on the power button below. Wait 10 seconds and press the power button on the device.'),
    html.P('Add titles and axes to graphs'),
    html.Button('Power', id='button', style={'width': '10%', 'display': 'inline-block', 'color':'red'}),
    html.Div(id='home-content'),
])

#callback for power button
@app.callback(
    Output('home-content', 'children'),
    [Input('button', 'n_clicks')])
def update_output(n_clicks):
    if(n_clicks == 1):
        os.system('sudo shutdown -h now')
        return "Powering off...Please wait 10 seconds and press the power button on the device."