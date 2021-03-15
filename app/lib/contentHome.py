#!/usr/bin/env python
# -*- coding: utf-8 -*-

#---------------------------------
#Start of contentHome.py
#--------------------------------- 

#################################################
#Libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app
from dash.dependencies import Input, Output, State
##################################################

#Main function to be able to call all the application fuctionality:
def contentHome():
    return dbc.Collapse([
        html.Br(),                
        html.Div(html.Img(src=app.get_asset_url("Logo-UAO-Stats.png"), width="200", height="120"),className="d-flex justify-content-center"),        
        html.Div(html.H6("Data Science as a decision tool for universities´ sustainability"),className="d-flex justify-content-center"),        
        html.Br(),
        dbc.Jumbotron(
            dbc.Container([
                    html.H1("UAO Stats",
                        className="display-3 ",
                        style={'color':'white'}
                    ),
                    
                ],
                fluid=True
            ),
            fluid=True,
            style={
                'background-image': 'url("/assets/home-header.jpg")',
                'background-size': 'cover',
                'height': '100%'
            }
        ),       
        html.Br(),
        html.H6('Through these functions, UAO can analyze the data received, predict trends and propose solutions that generate an impact on the problem posed:'),
        html.Br(),
        
        dbc.Row([
            dbc.Col([
                    
                    html.Div(html.Img(src=app.get_asset_url("map.jpg"), width="100", height="100"),className="d-flex justify-content-center",), 
                    html.Div(html.H5('Map'),className="d-flex justify-content-center",),
                    html.Hr(),
                    html.Div(html.H6('Visualize the city/town-spatial distribution of university students'),className="d-flex justify-content-center",),
                    html.Hr(),
                    html.Div(html.A(html.Button('View more', className='btn-outline-danger'),href='#', id="linkContentVisualization1_map"),className="d-flex justify-content-center",)
                ],md=2),
            dbc.Col([
                    
                    html.Div(html.Img(src=app.get_asset_url("visualization.jpg"), width="100", height="100"),className="d-flex justify-content-center",), 
                    html.Div(html.H5('Visualization'),className="d-flex justify-content-center",),
                    html.Hr(),
                    html.Div(html.H6('Explore the general university students’ characteristics or features'),className="d-flex justify-content-center",),
                    html.Hr(),
                    html.Div(html.A(html.Button('View more', className='btn-outline-danger'),href='#', id="linkContentVisualization1"),className="d-flex justify-content-center",)
                ],md=2),
            dbc.Col([
                    
                    html.Div(html.Img(src=app.get_asset_url("segmentation.jpg"), width="100", height="100"),className="d-flex justify-content-center",), 
                    html.Div(html.H5('Segmentation'),className="d-flex justify-content-center",),
                    html.Hr(),
                    html.Div(html.H6('Discover an analysis of the enrolled university students’ profile'),className="d-flex justify-content-center",),
                    html.Hr(),
                    html.Div(html.A(html.Button('View more', className='btn-outline-danger'),href='#', id="linkContentSegmentation1"),className="d-flex justify-content-center",)
                ],md=2), 
            dbc.Col([
                    
                    html.Div(html.Img(src=app.get_asset_url("characterization.jpg"), width="100", height="100"),className="d-flex justify-content-center",), 
                    html.Div(html.H5('Characterization'),className="d-flex justify-content-center",),
                    html.Hr(),
                    html.Div(html.H6('Find common relations among characteristics as a meaningful tool'),className="d-flex justify-content-center",),
                    html.Hr(),
                    html.Div(html.A(html.Button('View more', className='btn-outline-danger'),href='#', id="linkContentCharacterization1"),className="d-flex justify-content-center",)
                ],md=2),
            dbc.Col([
                    
                    html.Div(html.Img(src=app.get_asset_url("prediction.jpg"), width="100", height="100"),className="d-flex justify-content-center",), 
                    html.Div(html.H5('Prediction'),className="d-flex justify-content-center",),
                    html.Hr(),
                    html.Div(html.H6('Predict the enrollment as an aid for scouting potential students'),className="d-flex justify-content-center",),
                    html.Hr(),
                    html.Div(html.A(html.Button('View more', className='btn-outline-danger'),href='#', id="linkContentPrediction1"),className="d-flex justify-content-center",)
                ],md=2),           
            dbc.Col([
                    
                    html.Div(html.Img(src=app.get_asset_url("workteam.jpg"), width="100", height="100"),className="d-flex justify-content-center",), 
                    html.Div(html.H5('Work Team'),className="d-flex justify-content-center",),
                    html.Hr(),
                    html.Div(html.H6('Meet the great team that worked to be able to run this application'),className="d-flex justify-content-center",),
                    html.Hr(),
                    html.Div(html.A(html.Button('View more', className='btn-outline-danger'),href='#', id="linkContentTeam1"),className="d-flex justify-content-center",)
                ],md=2),
            html.Hr(),
        ]),
       
    ], id="contentHome", className="container content", is_open=True)  # default page

#---------------------------------
#End of contentHome.py
#--------------------------------- 
