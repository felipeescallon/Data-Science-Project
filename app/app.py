#######################################################
# Main APP definition.
#
# Dash Bootstrap Components used for main theme and better
# organization.
#######################################################

#Libraries
import dash
import dash_bootstrap_components as dbc


###############
#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#server = app.server
##############

#running the app
app = dash.Dash(__name__)

app.css.config.serve_locally = False
app.title = 'UAO Stats' # default project name

# Boostrap CSS.
#app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})
#app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
app.css.append_css({'external_url': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css'})
app.css.append_css({'external_url': 'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css'})
#app.css.append_css({'external_url': 'http://code.jquery.com/jquery-3.3.1.min.js'})
#app.css.append_css({'external_url': 'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js'})

# We need this for function callbacks not present in the app.layout
app.config.suppress_callback_exceptions = True

##########################
#This is the end of app.py
##########################