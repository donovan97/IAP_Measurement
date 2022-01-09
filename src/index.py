import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import database, measurement, home, posttest, config
import pandas
import glob

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

#callback sets the layout for the main menu
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
         return home.layout
    elif pathname == '/measurement':
         return measurement.layout
    elif pathname == '/database':
         return database.layout
    elif pathname == '/posttest':
         return posttest.layout
    else:
        return '404'
                
if __name__ == '__main__':
    app.run_server(port = 8077, host='192.168.0.103')
    #get the ip above by running hostname -I on RBP. Call sudo python3 index.py to run the program.