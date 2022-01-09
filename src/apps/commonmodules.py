import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#Returns menu common to all pages
def get_menu():
    menu = html.Div([

        dcc.Link('Home', href='/', className="button"),
        dcc.Link('IAP measurement', href='/measurement', className="button"),
        dcc.Link('Database', href='/database', className="button"),
    ], className="row all-tabs")
    return menu    