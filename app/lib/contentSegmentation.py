#!/usr/bin/env python
# -*- coding: utf-8 -*-
#---------------------------------
#Start of contentSegmentation.py
#--------------------------------- 
############################################################################
#Libraries:
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
#import plotly.graph_objs as go #not used so far
#this is required to be able to use callbacks inside every Python script
from app import app
from dash.dependencies import Input, Output, State
import pandas as pd
############################################################################

#Defining data and clustering:
#General Data
df = pd.read_csv("data/matriculado_cluster.csv", sep=";",encoding="latin1")

#Cluster 1
df_segment1 = df[(df.Cluster == 0)]

#fig_vis = px.box(df,x=df.columns[0],y=df.columns[1],color_discrete_sequence=px.colors.diverging.RdYlBu)

#Cluster 1 Program
df_segment1_faculty = df_segment1['faculty'].value_counts()
df_segment1_faculty = df_segment1_faculty.reset_index()
df_segment1_faculty = df_segment1_faculty.rename(columns={'index': 'Faculty', 'faculty': 'Count'})
lineplot1_faculty=px.bar(df_segment1_faculty,x="Faculty",y='Count',color_discrete_sequence=px.colors.diverging.RdYlBu)

#Cluster 1 Gender
df_segment1_gender = df_segment1['gender'].value_counts()
df_segment1_gender = df_segment1_gender.reset_index()
df_segment1_gender = df_segment1_gender.rename(columns={'index': 'Gender', 'gender': 'Count'})
lineplot1_gender = px.bar(df_segment1_gender,x="Gender",y='Count',color_discrete_sequence=px.colors.diverging.RdYlBu)

#Cluster 1 Age
df_segment1_age = df_segment1['age'].value_counts()
df_segment1_age = df_segment1_age.reset_index()
df_segment1_age = df_segment1_age.rename(columns={'index': 'Age', 'age': 'Count'})
lineplot1_age = px.bar(df_segment1_age,x="Age",y='Count',color_discrete_sequence=px.colors.diverging.RdYlBu)

#Cluster 1 Stratum
df_segment1_stratum = df_segment1['stratum'].value_counts()
df_segment1_stratum = df_segment1_stratum.reset_index()
df_segment1_stratum = df_segment1_stratum.rename(columns={'index': 'Stratum', 'stratum': 'Count'})
lineplot1_stratum = px.bar(df_segment1_stratum,x="Stratum",y='Count',color_discrete_sequence=px.colors.diverging.RdYlBu)


#Cluster 2
df_segment2 = df[(df.Cluster == 1)]

#Cluster 2 Program
df_segment2_faculty= df_segment2['faculty'].value_counts()
df_segment2_faculty  = df_segment2_faculty.reset_index()
df_segment2_faculty = df_segment2_faculty.rename(columns={'index': 'Faculty', 'faculty': 'Count'})
lineplot2_faculty=px.bar(df_segment2_faculty,x="Faculty",y='Count',color_discrete_sequence=px.colors.diverging.RdYlBu)

#Cluster 2 Gender
df_segment2_gender = df_segment2['gender'].value_counts()
df_segment2_gender = df_segment2_gender.reset_index()
df_segment2_gender = df_segment2_gender.rename(columns={'index': 'Gender', 'gender': 'Count'})
lineplot2_gender = px.bar(df_segment2_gender,x="Gender",y='Count',color_discrete_sequence=px.colors.diverging.RdYlBu)

#Cluster 2 Age
df_segment2_age = df_segment2['age'].value_counts()
df_segment2_age = df_segment2_age.reset_index()
df_segment2_age = df_segment2_age.rename(columns={'index': 'Age', 'age': 'Count'})
lineplot2_age = px.bar(df_segment2_age,x="Age",y='Count',color_discrete_sequence=px.colors.diverging.RdYlBu)

#Cluster 2 Stratum
df_segment2_stratum = df_segment2['stratum'].value_counts()
df_segment2_stratum = df_segment2_stratum.reset_index()
df_segment2_stratum = df_segment2_stratum.rename(columns={'index': 'Stratum', 'stratum': 'Count'})
lineplot2_stratum = px.bar(df_segment2_stratum,x="Stratum",y='Count',color_discrete_sequence=px.colors.diverging.RdYlBu)

#main function:
def contentSegmentation():
    return dbc.Collapse([
        html.Br(),
        html.H1("Segmentation",id="titulo_segmentation"),
        html.Hr(),
        html.H4("In this section, you can find the cluster analysis carried out through the K-Modes methodology. As a result, it concludes that the population of enrolled students is divided into two groups, this thanks to the work on the analysis of the elbow and Silhouette methods, which gave that number as the optimal value of segments to be used. Please select the segment you want to see:",id="parrafo_segmentation"),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(html.A(html.Button('Segment 1', className="btn-outline-danger"),href='#', id="linksegment1"), width=6, lg=2),
                dbc.Col(html.A(html.Button('Segment 2', className="btn-outline-danger"),href='#', id="linksegment2"), width=6, lg=2),

            ], className="d-flex justify-content-center"
        ),
        html.Hr(),
            dbc.Collapse([
                html.H1("Segment 1", className="d-flex justify-content-center"),
                html.Br(),
                html.Div(
                html.Img(src=app.get_asset_url("segment_1.jpeg"), id="segment1-image", width="650", height="650"),
                className="d-flex justify-content-center",
                ),                
                html.Br(),
                html.H3("This group corresponds to 10,511 people, which represents 71% of the total enrolled", className="d-flex justify-content-center"),
                html.Hr(),
                html.H6("Segment 1 is mainly characterized by having people belonging to the engineering faculty in 63%, followed by the administrative sciences faculty (15%) in programs such as industrial engineering, mechanical engineering and mechatronics engineering. On the other hand, this cluster is given mainly by people of the male gender (72%) and belonging to socioeconomic strata 3 and 4 (37% and 20% respectively)."),
                html.Hr(),
                dbc.Row([
                dbc.Col(dcc.Graph(figure=lineplot1_faculty, id='knowledge1'),md=6),
                dbc.Col(dcc.Graph(figure=lineplot1_gender, id='gender1'),md=6)
                ]),
                dbc.Row([
                dbc.Col(dcc.Graph(figure=lineplot1_age, id='age1'),md=6),
                dbc.Col(dcc.Graph(figure=lineplot1_stratum, id='stratum1'),md=6)
                ]),
                ],id='group_segment1', className="container content", is_open=False),
            dbc.Collapse([
                html.H1("Segment 2", className="d-flex justify-content-center"),
                html.Br(),
                html.Div(
                html.Img(src=app.get_asset_url("segment_2.jpeg"), id="segment2-image", width="650", height="650"),
                className="d-flex justify-content-center",
                ),
                html.Hr(),
                html.H3("This group corresponds to 4.099 people, which represents 29% of the total enrolled", className="d-flex justify-content-center"),
                html.Hr(),
                html.H6("Segment 2 is characterized by containing people who are mainly in the faculty of administrative sciences and the faculty of communication and social sciences (54% and 18% respectively) in programs such as marketing and international business, social communication and journalism and business administration . Represented mainly by the female gender with 70% of the total of the people belonging to this cluster. On the other hand, this cluster is represented by people belonging to socioeconomic strata 2 and 3 in 75% and 25% respectively."),
                html.Hr(),
                dbc.Row([
                dbc.Col(dcc.Graph(figure=lineplot2_faculty, id='knowledge2'),md=6),
                dbc.Col(dcc.Graph(figure=lineplot2_gender, id='gender2'),md=6),
                dbc.Col(dcc.Graph(figure=lineplot2_age, id='age2'),md=6),
                dbc.Col(dcc.Graph(figure=lineplot2_stratum, id='stratum2'),md=6)
                ]),
                ],id='group_segment2', className="container content", is_open=False),
                ], id="contentSegmentation", className="container content", is_open=False)

#clicks handling:
d_clicks = {}
d_clicks['Segment1']=None
d_clicks['Segment2']=None


#Callback setting:
@app.callback(
    Output('group_segment1', 'is_open'),
    [Input("linksegment1", "n_clicks"),
     Input("linksegment2", "n_clicks")],
    [State("group_segment1", "is_open")],)

def toggle_collapse(n_Segment1, n_Segment2, is_open):
    global d_clicks
    if n_Segment1==None:
        return False
    if d_clicks['Segment1'] != n_Segment1:
        d_clicks['Segment1'] = n_Segment1
        return True
    if (d_clicks['Segment1']==None and d_clicks['Segment2']==None):
        return False
    return False


@app.callback(
    Output('group_segment2', 'is_open'),
    [Input("linksegment1", "n_clicks"),
     Input("linksegment2", "n_clicks")],
    [State("group_segment2", "is_open")],)

def toggle_collapse(n_Segment1, n_Segment2, is_open):
    global d_clicks
    if n_Segment2==None:
        return False
    if d_clicks['Segment2'] != n_Segment2:
        d_clicks['Segment2'] = n_Segment2
        return True
    if (d_clicks['Segment1']==None and d_clicks['Segment2']==None):
        return False
    return False

#---------------------------------
#End of contentSegmentation.py
#--------------------------------- 
