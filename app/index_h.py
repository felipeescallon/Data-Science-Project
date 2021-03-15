#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################################################################################

#Copied for Dash:
# Basics Requirements
import pathlib
import os
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px

# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# Data
import math
import numpy as np
from datetime import datetime as dt
import pandas as pd
import json

# Recalling app.py as it is the standard way:
from lib import menu, contentHome, contentVisualization_map, contentVisualization, contentSegmentation, contentCharacterization, contentPrediction, contentTeam
from app import app

layout='horizontal' # Accordingly, this Python script is called "index_h.py"
#layout='vertical' # if UAO likes it better, just in case, so it will be called "index_v.py"

#function to call the menu horizontally
def menu_h(id, links):
    lst_items=[]
    for i in range(len(links)):
        l=links[i]
        #if i>=1:
        #    lst_items.append( dbc.NavItem("/") )
        #lst_items.append( dbc.NavItem(dbc.NavLink( l['label'], id=l['id'], href="#", active= True),style={'list-style-type': 'none'}) )
        lst_items.append( dbc.NavItem(dbc.NavLink( l['label'], id=l['id'], href="#", active= True),className="my_navlink") )
    return dbc.Navbar([
        html.A(
            dbc.NavbarBrand(html.Img(src="/assets/img/logo2.png", id="img-brand")),
            href="#"
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(lst_items, id="navbar-collapse", navbar=True)
    ],id=id, color="#b22222",dark=True, className="fixed-top navbar-expand-lg my-navbar")
    #],id=id, className="navbar fixed-top navbar-expand-lg navbar-dark bg-dark")

#First callback
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

#########################################################################################################################################

#links for the menu
link_menu=[{'label': 'Home', 'id':'linkContentHome'},
    {'label': 'Map', 'id':'linkContentVisualization_map'},
    {'label': 'Visualization', 'id':'linkContentVisualization'},
    {'label': 'Segmentation', 'id':'linkContentSegmentation'},    
    {'label': 'Characterization', 'id':'linkContentCharacterization'},
    {'label': 'Prediction', 'id':'linkContentPrediction'},
    {'label': 'Work Team', 'id':'linkContentTeam'}]

#placing a DS4A image
DS4A_Img = html.Div(
    children=[html.Img(src=app.get_asset_url("ds4a-img.svg"), id="ds4a-image",)],
)

#For the vertical layout to work properly:
layout_v = html.Div([
        html.Div([
                html.Div([
                        DS4A_Img,  # Add the DS4A_Img located in the assets folder
                        html.Hr(),  # Add an horizontal line
                        html.Img(src='/assets/img/logo_UAO.png'),
                        #html.Img(src='/assets/img/ds4A-logo.png'),
                        menu.menu()#better to save as menu.py and have it inside lib along with the other python scripts
                ],id="izquierdo", className="col-md-4"),
                html.Div([
                        #better to be called from a python scripts, this way "contentHome.contentHome()" instead of just "contentHome()"
                        contentHome.contentHome(),
                        contentVisualization_map.contentVisualization_map(),
                        contentVisualization.contentVisualization(),
                        contentSegmentation.contentSegmentation(),                        
                        contentCharacterization.contentCharacterization(),
                        contentPrediction.contentPrediction(),
                        contentTeam.contentTeam()
                ], id="derecho", className="col-md-8")
        ], className="row")
], id='vertical_layout', className="container-fluid")
#], className="container")

#For the horizontal layout to work properly:
layout_h = html.Div([
        menu_h(id="menu", links=link_menu),
        contentHome.contentHome(),
        contentVisualization_map.contentVisualization_map(),
        contentVisualization.contentVisualization(),
        contentSegmentation.contentSegmentation(),        
        contentCharacterization.contentCharacterization(),
        contentPrediction.contentPrediction(),
        contentTeam.contentTeam()
], id='horizontal_layout', className="container-fluid")

#Chossing the preferred layput
if layout == 'horizontal':
    app.layout = layout_h
else:
    app.layout = layout_v


#Clicks handling:
d_clicks = {}
d_clicks['home']=None
d_clicks['visualization_map']=None
d_clicks['Visualization1_map']=None
d_clicks['visualization']=None
d_clicks['Visualization1']=None
d_clicks['segmentation']=None
d_clicks['Segmentation1']=None
d_clicks['characterization']=None
d_clicks['Characterization1']=None
d_clicks['prediction']=None
d_clicks['Prediction1']=None
d_clicks['team']=None
d_clicks['Team1']=None

########################################################################################################################################
#START OF CALLBACK (to be able for the index to run properly through the app):
@app.callback([
    Output("contentHome", "is_open"),
    Output("contentVisualization_map", "is_open"),
    Output("contentVisualization", "is_open"),
    Output("contentSegmentation", "is_open"),
    Output("contentCharacterization", "is_open"),
    Output("contentPrediction", "is_open"),
    Output("contentTeam", "is_open"),
    ],
    [Input("linkContentHome", "n_clicks"),
     Input("linkContentVisualization_map", "n_clicks"),
     Input("linkContentVisualization1_map", "n_clicks"),
     Input("linkContentVisualization", "n_clicks"),
     Input("linkContentVisualization1", "n_clicks"),
     Input("linkContentSegmentation", "n_clicks"),     
     Input("linkContentSegmentation1", "n_clicks"),     
     Input("linkContentCharacterization", "n_clicks"),
     Input("linkContentCharacterization1", "n_clicks"),
     Input("linkContentPrediction", "n_clicks"),
     Input("linkContentPrediction1", "n_clicks"),
     Input("linkContentTeam", "n_clicks"),
     Input("linkContentTeam1", "n_clicks")],
    [State("contentTeam", "is_open")],
)
def toggle_collapse(n_home, n_visualization_map, n_visualization1_map, n_visualization, n_visualization1, n_segmentation, n_segmentation1, n_characterization, n_characterization1, n_prediction, n_prediction1, n_team, n_team1, is_open):
    global d_clicks

    home_open = False
    visu_map_open = False
    visu_open = False
    segm_open = False
    char_open = False
    pred_open = False
    team_open = False

    if d_clicks['home'] != n_home:
        d_clicks['home'] = n_home
        home_open = True

    if d_clicks['visualization_map'] != n_visualization_map:
        d_clicks['visualization_map'] = n_visualization_map
        visu_map_open = True
    if d_clicks['Visualization1_map'] != n_visualization1_map:
        d_clicks['Visualization1_map'] = n_visualization1_map
        visu_map_open = True

    if d_clicks['visualization'] != n_visualization:
        d_clicks['visualization'] = n_visualization
        visu_open = True
    if d_clicks['Visualization1'] != n_visualization1:
        d_clicks['Visualization1'] = n_visualization1
        visu_open = True

    if d_clicks['segmentation'] != n_segmentation:
        d_clicks['segmentation'] = n_segmentation
        segm_open = True
    if d_clicks['Segmentation1'] != n_segmentation1:
        d_clicks['Segmentation1'] = n_segmentation1
        segm_open = True

    if d_clicks['characterization'] != n_characterization:
        d_clicks['characterization'] = n_characterization
        char_open = True
    if d_clicks['Characterization1'] != n_characterization1:
        d_clicks['Characterization1'] = n_characterization1
        char_open = True

    if d_clicks['prediction'] != n_prediction:
        d_clicks['prediction'] = n_prediction
        pred_open = True
    if d_clicks['Prediction1'] != n_prediction1:
        d_clicks['Prediction1'] = n_prediction1
        pred_open = True

    if d_clicks['team'] != n_team:
        d_clicks['team'] = n_team
        team_open = True
    if d_clicks['Team1'] != n_team1:
        d_clicks['Team1'] = n_team1
        team_open = True

    if not home_open and not visu_map_open and not visu_open and not segm_open and not char_open and not pred_open and not team_open:
        home_open = True

    return home_open, visu_map_open, visu_open, segm_open, char_open, pred_open, team_open

#END OF CALLBACK
######################################################################################################################################


# Configuring APP running as Web
if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server(host="0.0.0.0", port="8050", debug=True) #debug=True (for localshost); #)#debug=False (for AWS EC2)


##############################
#This is the end of index_h.py
##############################
