#!/usr/bin/env python
# -*- coding: utf-8 -*-
#---------------------
#Start of contentTeam.py
#---------------------
#Libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd 

#Defining the work team section:
def contentTeam():
    df = pd.read_csv("data/integrantes.csv", index_col=False)
    lst_comp = []
    for _,u in df.iterrows():
        lst_comp.append( html.Div(
            html.Div([
                html.Img(src="/assets/"+u['photo'], className="card-img-top rounded-circle mx-auto img_contact"),
                html.Div([
                    html.H4(u['name'],className="card-title"),
                    html.P(u['title'],className="card-text")
                ],className="card-body"),
                html.Div([
                    html.A(
                        html.I(className="fab fa-linkedin-in")
                        ,href=u['linkedin'], target="_blank", className="btn-outline-danger m-2"),
                    html.A(
                        html.I(className="fas fa-envelope")
                        ,href="mailto:"+u['email'], target="_blank", className="btn-outline-danger m-2")
                ],className="card-footer")
            ],className="card text-center")
        ,className="col-lg-3 col-md-4 col-sm-6 p-4") )    
    return dbc.Collapse([
        html.Br(),
        html.H1("Work Team",id="titulo_team"),
        html.Hr(),
        html.Div( lst_comp ,className="row")                       
    ],id="contentTeam", className="container content", is_open=False)

#---------------------
#END OF contentTeam.py
#---------------------