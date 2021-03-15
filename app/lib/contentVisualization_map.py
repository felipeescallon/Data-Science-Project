#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------------------------------------------------------------------
#START OF contentVisualization_map.py
#----------------------------------------------------------------------------------------------------------------------------------------

#importing the neccesary libraries
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json
import dash_table

#new libraries
import folium  #needed for interactive map
from folium.plugins import HeatMap
import numpy                 as np

#----------------------------------------------------------------------------------------------------------------------------------------
#RETRIEVING THE INFO FROM OUR DATABASE:
import re
import io
from unicodedata import normalize
from sqlalchemy import create_engine
#this is required to be able to use callbacks inside every Python script:
from app import app

###################################################################################################################
##Connection to AWS RDS
host = '****'                   #AWS RDS instance
port = 5432                     #default port
user = '****'                   #database user
password = '****'               #database password
database = '****'               #database name
connDB = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}') #database connection (only once)
###################################################################################################################

lang='en' # default ('sp' for Spanish), this is to choose option_fields_sp.csv or option_fields_sp.csv
##SQL_Query = pd.read_sql('SELECT * FROM enrolled_uao LIMIT 100', connDB)

option_fac_prog = 'fac'

#----------------------------------------------------------------------------------------------------------------------------------------
#copying from the database...
#FUNCTIONS TO GET INFO FROM RDS:
def dataframeCiudades_map(dataset, period, gender, stratum, fac_or_prog, faculty, program):
    '''
        Dataset is the name of the table we want to query
        ejeX is the kind of aggrupation we want to build; it can be = 'program', 'faculty'
        period and gender must be 'ALL' if no filter wants to be used
        period has to be 'YYYY-PP' where YYYY is year and PP is academic period (01 or 03)
        gender has to be either 'M' or 'F'
    '''    
    sql_period = " where period = '" + period + "' "
    if period == 'ALL':
        sql_period = " where period != '" + period + "' "

    sql_gender = " and gender = '" + gender + "' "
    if gender == 'ALL':
        sql_gender = " and gender != '" + gender + "' "

    sql_stratum = " and stratum = " + str(stratum) + " "
    if stratum == '0':
        sql_stratum = " and stratum != " + str(stratum) + " "

    sql_career = " "
    if fac_or_prog == 'fac':
        sql_career = " and   faculty = '" + faculty + "' "
        if faculty == 'ALL':
            sql_career = " and   faculty != '" + faculty + "' "
    else:
        sql_career = " and program = '" + program + "' "
        if program == 'ALL':
            sql_career = " and program != '" + program + "' "

    sql1 = "select t.city as ciudad, lat, lon, count(*) as conteo from " + dataset + " t join cities c on t.city = c.city " + \
        sql_period + \
        sql_gender + \
        sql_stratum + \
        sql_career + \
       " group by 1,2,3 having count(*) > 4 "
    
    sql1_df = pd.read_sql(sql1, connDB) #it is necessary to show all the colimns to be consumed by Dash plots
    
    #print (sql1)
    return sql1_df

#defining the periods for the slider
periods = ["122009-01","142009-03","162010-01","182010-03","202011-01","222011-03","242012-01","262012-03","282013-01","302013-03",
            "322014-01","342014-03","362015-01","382015-03","402016-01","422016-03","442017-01","462017-03","482018-01","502018-03",
            "522019-01","542019-03","562020-01","582020-03","802021-00"
          ]#"2021-00"is equivalent to 'ALL'


#to fix the slider steps from 12 to 60, with 25 steps spaced "2 units", thus resulting in this 25 prefixes: 12, 14, 16,...,56, 58, 60 
option_period_map = [ {'label': '2009-01', 'value': '2009-01'},
            {'label': '2009-03', 'value': '2009-03'},
            {'label': '2010-01', 'value': '2010-01'},
            {'label': '2010-03', 'value': '2010-03'},
            {'label': '2011-01', 'value': '2011-01'},
            {'label': '2011-03', 'value': '2011-03'},
            {'label': '2012-01', 'value': '2012-01'},
            {'label': '2012-03', 'value': '2012-03'},
            {'label': '2013-01', 'value': '2013-01'},
            {'label': '2013-03', 'value': '2013-03'},
            {'label': '2014-01', 'value': '2014-01'},
            {'label': '2014-03', 'value': '2014-03'},
            {'label': '2015-01', 'value': '2015-01'},
            {'label': '2015-03', 'value': '2015-03'},
            {'label': '2016-01', 'value': '2016-01'},
            {'label': '2016-03', 'value': '2016-03'},
            {'label': '2017-01', 'value': '2017-01'},
            {'label': '2017-03', 'value': '2017-03'},
            {'label': '2018-01', 'value': '2018-01'},
            {'label': '2018-03', 'value': '2018-03'},
            {'label': '2019-01', 'value': '2019-01'},
            {'label': '2019-03', 'value': '2019-03'},
            {'label': '2020-01', 'value': '2020-01'},
            {'label': '2020-03', 'value': '2020-03'},
            {'label': 'ALL', 'value': 'ALL'},
          ]
#defining stratum
option_stratum_map = [
                        {'label': 'ALL', 'value': '0'}, 
                        {'label': '1', 'value': '1'}, 
                        {'label': '2', 'value': '2'}, 
                        {'label': '3', 'value': '3'}, 
                        {'label': '4', 'value': '4'}, 
                        {'label': '5', 'value': '5'}, 
                        {'label': '6', 'value': '6'}, 
                    ]

#this is for the first set of filters:
datasets = ['enrolled_uao','registered_uao','deserters_uao']
option_database_map = [
                        {'label': 'Enrolled',   'value': datasets[0]},#df0='enrolled_uao'
                        {'label': 'Registered', 'value': datasets[1]},#df1='registered_uao'
                        {'label': 'Deserters',  'value': datasets[2]} #df2='deserters_uao'
                    ]

option_faculty_or_program_map = [
                        {'label': 'Faculty', 'value': 'fac'}, #this is just to know what to put in the X-axis when plotting           
                        {'label': 'Program', 'value': 'prog'} #this is just to know what to put in the X-axis when plotting                        
                    ]

option_gender_map = [
                        {'label': 'ALL', 'value': 'ALL'}, #ALL(both)-by default
                        {'label': 'Women', 'value': 'F'},#Female
                        {'label': 'Men', 'value': 'M'},#Male
                    ]               

option_program_map = [
        {'label': 'Administración de empresas'                     , 'value': 'administracion de empresas'},
        {'label': 'Cine y com. digital'                    , 'value': 'cine y comunicacion digital'},
        {'label': 'Com. publicitaria'                      , 'value': 'comunicacion publicitaria'},
        {'label': 'Com. social periodismo'                 , 'value': 'comunicacion social periodismo'},
        {'label': 'Contaduria pública'                             , 'value': 'contaduria publica'},
        {'label': 'Diseno com. gráfica'              , 'value': 'diseno de la comunicacion grafica'},
        {'label': 'Diseno industrial'                              , 'value': 'diseno industrial'},
        {'label': 'Economía'                                       , 'value': 'economia'},
        {'label': 'Ing. ambiental'                           , 'value': 'ingenieria ambiental'},
        {'label': 'Ing. biomédica'                           , 'value': 'ingenieria biomedica'},
        {'label': 'Ing. eléctrica'                           , 'value': 'ingenieria electrica'},
        {'label': 'Ing. electrónica y telco.'    , 'value': 'ingenieria electronica y telecomunicaciones'},
        {'label': 'Ing. industrial'                          , 'value': 'ingenieria industrial'},
        {'label': 'Ing. informática'                         , 'value': 'ingenieria informatica'}, 
        {'label': 'Ing. mecánica'                            , 'value': 'ingenieria mecanica'},
        {'label': 'Ing. mecatrónica'                         , 'value': 'ingenieria mecatronica'},
        {'label': 'Ing. multimedia'                          , 'value': 'ingenieria multimedia'},
        {'label': 'Mercadeo y negocios int.'            , 'value': 'mercadeo y negocios internacionales'},
        {'label': 'ALL'               , 'value': 'ALL'}        
                    ]

option_faculty_map = [
        {'label': 'F. de com. y ciencias sociales'  , 'value': 'facultad de comunicacion y ciencias sociales'},
        {'label': 'F. de ciencias administrativas'  , 'value': 'facultad de ciencias administrativas'},
        {'label': 'F. de ingeniería'                , 'value': 'facultad de ingenieria'},
        {'label': 'F. de humanidades y artes'       , 'value': 'facultad de humanidades y artes'},
        {'label': 'ALL'               , 'value': 'ALL'}        
                    ]


option4_slider_map = {
                        12200901 : {'label': periods[0][4:9], 'style': {'color': '#77b0b1'}}, 
                        14200903 : {'label': periods[1][4:9], 'style': {'color': '#77b0b1'}},
                        16201001 : {'label': periods[2][4:9], 'style': {'color': '#77b0b1'}},
                        18201003 : {'label': periods[3][4:9], 'style': {'color': '#77b0b1'}},
                        20201101 : {'label': periods[4][4:9], 'style': {'color': '#77b0b1'}},
                        22201103 : {'label': periods[5][4:9], 'style': {'color': '#77b0b1'}},
                        24201201 : {'label': periods[6][4:9], 'style': {'color': '#77b0b1'}},
                        26201203 : {'label': periods[7][4:9], 'style': {'color': '#77b0b1'}},
                        28201301 : {'label': periods[8][4:9], 'style': {'color': '#77b0b1'}},
                        30201303 : {'label': periods[9][4:9], 'style': {'color': '#77b0b1'}},
                        32201401 : {'label': periods[10][4:9],'style': {'color': '#77b0b1'}},
                        34201403 : {'label': periods[11][4:9], 'style': {'color': '#77b0b1'}},
                        36201501 : {'label': periods[12][4:9], 'style': {'color': '#77b0b1'}},
                        38201503 : {'label': periods[13][4:9], 'style': {'color': '#77b0b1'}},
                        40201601 : {'label': periods[14][4:9], 'style': {'color': '#77b0b1'}},
                        42201603 : {'label': periods[15][4:9], 'style': {'color': '#77b0b1'}},
                        44201701 : {'label': periods[16][4:9], 'style': {'color': '#77b0b1'}},
                        46201703 : {'label': periods[17][4:9], 'style': {'color': '#77b0b1'}},
                        48201801 : {'label': periods[18][4:9], 'style': {'color': '#77b0b1'}},
                        50201803 : {'label': periods[19][4:9], 'style': {'color': '#77b0b1'}},
                        52201901 : {'label': periods[20][4:9], 'style': {'color': '#77b0b1'}},
                        54201903 : {'label': periods[21][4:9], 'style': {'color': '#77b0b1'}},
                        56202001 : {'label': periods[22][4:9], 'style': {'color': '#77b0b1'}},
                        58202003 : {'label': periods[23][4:9], 'style': {'color': '#77b0b1'}},
                        61202100 : {'label': 'ALL', 'style': {'color': '#893737', 'font-weight': 'bold'}}#"2021-00"is equivalent to 'ALL' - by default                    
                    }

#dataframeCiudades2(dataset, period, gender, stratum, fac_or_prog, faculty, program):
df = dataframeCiudades_map('enrolled_uao', 'ALL', 'ALL', '0', 'fac', 'ALL', 'ALL')

#defining the handling function to be called:
def contentVisualization_map():    
    return dbc.Collapse([
                            html.Br(),
                            html.H1("Map",id="titulo_visualization_map"),        
                            html.Hr(),        
                            # html.Div([
                            #         dbc.Row([
                            #             dbc.Col(
                            #                 "Choose the desired database::",
                            #                 className="col-6"
                            #             ),
                            #         ]),
                            #         dbc.Row([
                            #             dbc.Col(
                            #                 dcc.RadioItems(
                            #                     id='option-database-map',
                            #                     options=option_database_map,
                            #                     value=datasets[0],#'enrolled_uao',
                            #                     labelStyle={'margin-left':'10px'}
                            #                 ),
                            #             ),
                            #         ]),
                            # ]),

                            #html.Hr(),        
                            html.Div([
                                        html.Div(
                                                    "Pick filtering options:",
                                                    className="col-6"
                                                ),
                                    ], 
                                    className="row"),                            

                            html.Div([
                                dbc.Row([
                                    dbc.Col( html.Div("Database:", className="col-6") ),
                                    dbc.Col(
                                            dcc.RadioItems(
                                                            id='option-faculty-or-program-map',
                                                            options=option_faculty_or_program_map,
                                                            value='fac',
                                                            labelStyle={'margin-left':'10px'}
                                            )
                                    ),
                                    dbc.Col( html.Div("Stratum:", className="col-6") ),
                                    dbc.Col( html.Div("Gender:", className="col-6") ),
                                ]),
                                dbc.Row([
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id='option-database-map',
                                            options=option_database_map,
                                            value=datasets[0],#'enrolled_uao',
                                            #labelStyle={'margin-left':'10px'}
                                        ),
                                    ),

                                    dbc.Col([
                                            dcc.Dropdown(
                                                id='option-faculty-map', 
                                                options=option_faculty_map, 
                                                value='ALL',
                                                style={'display': 'block'}
                                            ),                                                
                                            dcc.Dropdown(
                                                id='option-program-map', 
                                                options=option_program_map, 
                                                value='ALL',
                                                style={'display': 'none'}
                                            ),                                                
                                    ]),
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id='option-stratum-map', #to differentiate from the above dropdown
                                            options=option_stratum_map, # city, gender, age, stratum
                                            value='0',
                                            #style={'height': '30px', 'width': '100px'}
                                            #className="col-6"
                                        ),
                                    ),
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id = 'option-gender-map',
                                            options=option_gender_map,
                                            value='ALL', #default
                                            #labelStyle={'margin-left':'10px'},
                                            #className="col-6" #, this comma should not be here
                                        ),
                                    ),
                                ])
                            ]),
                            html.Br(),
                            html.Div([  
                                        dcc.Slider(# in the callback, df must be the ddf
                                            id = 'option4-slider-map',
                                            min = 12200901, #must be integer(YYYY0X), X={1,3} for 1st and 2nd semester (period)
                                            max = 61202100, #then, for instance, it will be turn into "2020-03"              
                                            step = None, #default one by one                                                                                                                                                           
                                            marks=option4_slider_map,
                                            value= 61202100, #default('ALL')  
                                            included=False                                        
                                        ),
                                        html.Iframe(id='map', srcDoc=open('assets/start_map.html', 'r').read(), width='100%', height='600'),
                                    ]),
                            html.Hr(), 
                            

                            #Optionally- showing the dataframe in a table:
                            html.Div([
                                        html.Div(
                                                    "Table:",
                                                    className="col-6"
                                                ),
                                    ], 
                                    className="row"),                                      
                            dash_table.DataTable(
                                                    id='table-map',
                                                    data=df.to_dict('records'),
                                                    columns=[{'id': c, 'name': c} for c in df.columns],
                                                ),#this comma needs to be here
                            html.Hr(),                            
                        ],id="contentVisualization_map", className="container content", is_open=False) #className="content"

#Callback sets:
@app.callback(
                [
                #dash.dependencies.Output('option-program-map', 'disabled'),
                #dash.dependencies.Output('option-faculty-map', 'disabled')
                dash.dependencies.Output('option-program-map', 'style'),
                dash.dependencies.Output('option-faculty-map', 'style')

                ],
                [
                Input('option-faculty-or-program-map', 'value'),    #value2=program-faculty (selected_fac_program)
                ]#in the order of the inputs, value represents the folloeing argumnets of the update_graph fucntion:
            ) 
def disable_dropdown(selected_fac_program):
    global option_fac_prog
    if selected_fac_program == 'fac':
        option_fac_prog = 'fac'
        return {'display': 'none'}, {'display': 'block'}
    else:
        option_fac_prog = 'prog'
        return {'display': 'block'}, {'display': 'none'}


@app.callback(
                [
                #Output('main-graph-vis', 'figure'),    #graph  
                dash.dependencies.Output('map', 'srcDoc'),          
                Output('table-map', 'data'),            #table-data
                Output('table-map', 'columns')          #table-columns
                ],
                [
                Input('option4-slider-map', 'value'),   #value4=period (selected_period)                    
                #Input('option-period-map', 'value'),#value0=plot-type (selected_plot_type)
                Input('option-database-map', 'value'),    #value1=dataset (selected_dataset)
                Input('option-stratum-map', 'value'), #value3=city-sex-age-stratum (selected_city_st_age)
                Input('option-gender-map', 'value'),   #value4=period (selected_period)                
                Input('option-program-map', 'value'),   #value4=period (selected_period)                
                Input('option-faculty-map', 'value'),   #value4=period (selected_period)         
                #Input('option5-radio-vis', 'value')     #value6=men-women-all (selected_gender)                            
                ]#in the order of the inputs, value represents the folloeing argumnets of the update_graph fucntion:
            ) 

def update_graph_map(selected_period, selected_dataset, selected_stratum, selected_gender, selected_program, selected_faculty):#5--- #selected_tperiod, selected_gender):# 6 options in total

    global option_fac_prog
    
    if selected_period!=61202100:
        selected_period_str=str(selected_period)[2:6]+'-'+str(selected_period)[6:8]#slicing goes up to sup lim - 1
    else:
        selected_period_str = 'ALL'

    #initializing the first graph to show by default!!!
    #print ("option_fac_prog : " + option_fac_prog)
    df = dataframeCiudades_map(selected_dataset, selected_period_str, selected_gender, selected_stratum, option_fac_prog, selected_faculty, selected_program)
    
    columns=[{"name": i, "id": i} for i in df.columns] #(*)
    data=df.to_dict('records') #df is going to be shown 

    #create the map and starts in Cali, Colombia
    folium_map = folium.Map(
                            location=[3.4354, -76.5196],
                            zoom_start=7.5,
                            tiles="OpenStreetMap")
    #Now we can have a scatter plot of the first 1000 data points on the above map

    for i in range(0,df.shape[0]):
        #It defines scale for circles
        multiplier = 3
        radius1 = np.log(df["conteo"][i])*multiplier
        marker = folium.CircleMarker(location=[df["lat"][i],df["lon"][i]],
                                    radius=radius1,color="#3186cc",fill=True,fill_color='#FF0000',
                                    tooltip=str.upper(df["ciudad"][i]) + " - " + str(df["conteo"][i]))
        marker.add_to(folium_map)

    folium_map.save('assets/temp.html')

    return open('assets/temp.html', 'r').read(), data, columns  #fig_vis==return_slider (sliders updates the graph)

#----------------------------------
#END OF contentVisualization_map.py
#----------------------------------