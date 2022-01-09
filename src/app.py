import dash
import dash_core_components as dcc
import dash_html_components as html

print(dcc.__version__)

app = dash.Dash(__name__)

server = app.server
app.config.suppress_callback_exceptions = True

#Start the dash server