#!/usr/bin/env python
# -*- coding: utf-8 -*-

#---------------------------------
#Start of menu.py
#--------------------------------- 

#################################################
#Libraries
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
#################################################

#Main fucntion for the menu
def menu():
    return html.Ul([
        html.Li(
            html.A([
                html.I(className='fas fa-home'),
                ' Home'
            ], id="linkContentHome",href="#", className="nav-link")
        ,className="nav-item"),
        #html.Ul([#IT WORKED FOR IDENTATION
        html.Li(
            html.A([
                html.I(className='fas fa-image'),
                ' Map'
            ], id="linkContentVisualization_map",href="#", className="nav-link")
        ,className="nav-item"),
        html.Li(
            html.A([
                html.I(className='fas fa-image'),
                ' Visualization'
            ], id="linkContentVisualization",href="#", className="nav-link")
        ,className="nav-item"),
        #],className="nav flex-column pl-5"),#IT WORKED FOR IDENTATION        
        html.Li(
            html.A([
                html.I(className='fas fa-signal'),
                ' Segmentation'
            ], id="linkContentSegmentation",href='#',className="nav-link")
        ,className="nav-item"),
        html.Li(
            html.A([
                html.I(className='fas fa-question'),
                ' Characterization'
            ], id="linkcontentCharacterization",href='#',className="nav-link")
        ,className="nav-item"),        
        html.Li(
            html.A([
                html.I(className='fas fa-question'),
                ' Prediction'
            ], id="linkContentPrediction",href='#',className="nav-link")
        ,className="nav-item"),        
        html.Li(
            html.A([
                html.I(className='fas fa-users'),
                ' Work Team'
            ], id="linkContentTeam",href='#', className="nav-link")
        ,className="nav-item")
        ], className="nav flex-column")

#---------------------------------
#End of menu.py
#--------------------------------- 

