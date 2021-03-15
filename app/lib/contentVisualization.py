#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------------------------------------------------------------------
#START OF contentVisualization.py
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
#Example: SQL_Query = pd.read_sql('SELECT * FROM enrolled_uao LIMIT 100', connDB)
#----------------------------------------------------------------------------------------------------------------------------------------
#Copying from the database...
#FUNCTIONS TO GET INFO FROM RDS:
cities_valle_no_cali = \
"'alcala','andalucia','ansermanuevo','argelia','bolivar','buenaventura','buga','bugalagrande','caicedonia','darien'," \
"'candelaria','cartago','dagua','el aguila','el cairo','el cerrito','el dovio','florida','ginebra','guacari','jamundi','la cumbre'," \
"'la union','la victoria','obando','palmira','pradera','restrepo','riofrio','roldanillo','san pedro','sevilla','toro','trujillo'," \
"'tulua','ulloa','versalles','vijes','yotoco','yumbo','zarzal'"

def dataframeCiudades(dataset, ejeX, period, gender):
    '''
        Dataset is the name of the table we want to query
        ejeX is the kind of aggrupation we want to build; it can be = 'program', 'faculty'
        period and gender must be 'ALL' if no filter wants to be used
        period has to be 'YYYY-PP' where YYYY is year and PP is academic period (01 or 03)
        gender has to be either 'M' or 'F'
    '''    
    sql_period = " where period = '" + period + "'"
    if period == 'ALL':
        sql_period = " where period != '" + period + "' "

    sql_gender = " and gender = '" + gender + "'"
    if gender == 'ALL':
        sql_gender = " and gender != '" + gender + "' "
        
    sql_ejeX = "program as programa "
    if ejeX == 'faculty':
        sql_ejeX = "faculty as facultad "
    
    #',' + sql_period + ',' + sql_gender+    
    sql1 = "select " + sql_ejeX + ", CASE WHEN city='cali' THEN 'cali' "\
       "WHEN city in (" + cities_valle_no_cali + ") THEN 'valle sin cali' " \
       "ELSE 'otra' " \
       "END as ciudad, count(*) as conteo from " + dataset + \
       sql_period + \
       sql_gender + \
       " group by 1,2 order by 3 desc"
    
    sql1_df = pd.read_sql(sql1, connDB) #it is necessary to show all the colimns to be consumed by Dash plots

    return sql1_df

def dataframeSexo_Edad_Estrato(dataset, ejeX, period, variable, gender, selected_plot_type):
    '''
        Dataset is the name of the table we want to query
        ejeX is the kind of aggrupation we want to build; it can be = 'program', 'faculty'
        period must be 'ALL' if no filter wants to be used
        period has to be 'YYYY-PP' where YYYY is year and PP is academic period (01 or 03)
        variable can be one of the following: gender, age and stratum
        gender has to be either 'M' or 'F'
    '''    
    sql_period = " where period = '" + period + "'"
    if period == 'ALL':
        sql_period = " where period != '" + period + "' "
        
    sql_gender = " and gender = '" + gender + "'"
    if gender == 'ALL':
        sql_gender = " and gender != '" + gender + "' "

    sql_ejeX = "program as programa "
    if ejeX == 'faculty':
        sql_ejeX = "faculty as facultad "
        
    sql_variable = "gender as sexo "
    if variable == 'age':
        if selected_plot_type == 'ycount':
            sql_variable = "CASE WHEN age < 18 THEN '< 18' "\
                                "WHEN age between 18 and 20 THEN '18-20' " \
                                "WHEN age between 21 and 23 THEN '21-23' " \
                                "WHEN age between 24 and 26 THEN '24-26' " \
                                "ELSE '>= 27' END as edad " 
        else:
            sql_variable = "age as edad "    
    elif variable == 'stratum':
        sql_variable = "stratum as estrato "
        
    sql1 = "select " + sql_ejeX + ", " + sql_variable + ", count(*) as conteo from " + dataset + \
       sql_period + \
       sql_gender + \
       " group by 1,2 order by 3 desc"
    
    sql1_df = pd.read_sql(sql1, connDB)#it is necessary to show all the colimns to be consumed by Dash plots
    
    return sql1_df

#EXAMPLE OF HOW TO CALL THE FUNCTIONS:

#How to call the function dataframeCiudades (def dataframeCiudades(dataset, ejeX, period, gender)):
#dataframeCiudades('enrolled_uao','faculty','2017-01','M') #here period is fixed as well as sex/gender

#Using other variables different from city, how to call the function dataframeSexo_Edad_Estrato(def dataframeSexo_Edad_Estrato(dataset, ejeX, period, variable, gender)):
#dataframeSexo_Edad_Estrato('registered_uao','program','2015-01','gender')#if not specified, it cover it all, in this case both genders M/F

#LET´S START WITH SOME TESTS FIRST CALLING THE FUNCTIONS ABOVE WITH FIXED PARAMETERS THAT...
#...WILL BE CHANGED AUTOMATICALLT THROUGH FILTERING LATER ON:

'''
#no need for this anymore since all the functionality goes inside the callbacks calling the two functions passing the parameters extracted from filters
SQL_subQuery1 = pd.read_sql('SELECT faculty, program, city, period, gender, age, year FROM enrolled_uao', connDB)
SQL_subQuery2 = pd.read_sql('SELECT faculty, program, city, period, gender, age, year FROM registered_uao', connDB) 
SQL_subQuery3 = pd.read_sql('SELECT faculty, program, city, period, gender, age, year FROM deserters_uao', connDB) 
'''
#WHAT IS NOW NECESSARY IS TO MANUALLY PUT SOME INFO AVAILABLE FOR THE DASH APP TO RUN PROPERLY 
# (initial parameters must be known, then filters take place)

#global by default:
datasets = ['enrolled_uao','registered_uao','deserters_uao']

#to fix the slider steps from 12 to 60, with 25 steps spaced "2 units", thus resulting in this 25 prefixes: 12, 14, 16,...,56, 58, 60 
periods = ["122009-01","142009-03","162010-01","182010-03","202011-01","222011-03","242012-01","262012-03","282013-01","302013-03",
            "322014-01","342014-03","362015-01","382015-03","402016-01","422016-03","442017-01","462017-03","482018-01","502018-03",
            "522019-01","542019-03","562020-01","582020-03","802021-00"
          ]#"2021-00"is equivalent to 'ALL'

#GOOD COMMENTS TO TAKE INTO ACCOUNT regarding the defined functions above:
'''
dataset IS INDEED A VALUE GIVEN by the selected radio button by the user           (dataset selected)
faculty_program is not selected by a specific number but as category to groupby    (just a flag to know if considered for the graph)
city is not selected by a specific number but as category to groupby               (just a flag to know if considered for the graph)
sex (gender) is not selected by a specific number but as category to groupby       (just a flag to know if considered for the graph)
age is not selected by a specific number but as category to groupby                (just a flag to know if considered for the graph)
stratum is not selected by a specific number but as category to groupby            (just a flag to know if considered for the graph)
period IS INDEED A VALUE GIVEN BY A SLIDER                                         (slider selected to for every period)
total_period is not selected by a specific number but as category to groupby       (if ON, then slider not working, if off, otherwise): 'ALL'
gender is not selected by a specific number but as category to groupby             (BUT POSSIBLE values to feed the functions: 'M', 'F', 'ALL') 
'''

#A general idea of a plot in Dash for px, there are: px.line, px.bar, px.scatter:
#that is done automatically by dash

#FILTERING:
#this is for the very first set of filters (option 0: 'ycount'(defaukt) and 'yother'):
#this is just to know what type of plot the user wants
#selected_plot_type:'ycount'(for a quantity plot: count vs fac/prog); 'yother'(for a distribution plot: var vs fac/prog)
option0_ddFields_vis = [
                        {'label': 'Quantity plot', 'value': 'ycount'}, #type of plot (Y-axis vs X-axis): count vs fac/prog
                        {'label': 'Distribution plot (only for Age)', 'value': 'yother'}, #type of plot (Y-axis vs X-axis): variable vs fac/prog
                    ]

#this is for the first set of filters:
option1_radio_vis = [
                        {'label': 'Enrolled',   'value': datasets[0]},#df0='enrolled_uao'
                        {'label': 'Registered', 'value': datasets[1]},#df1='registered_uao'
                        {'label': 'Deserters',  'value': datasets[2]} #df2='deserters_uao'
                    ]

#this is for the second set of filters:
option2_radio_vis = [
                        {'label': 'Faculty', 'value': 'faculty'}, #this is just to know what to put in the X-axis when plotting           
                        {'label': 'Program',   'value': 'program'} #this is just to know what to put in the X-axis when plotting                        
                    ]

#If possible to do it, english will be the language by default, and spanish the other option:
#Reading the option_fileds_en or option_fileds_sp depending on the global flag called lang('en','sp'):
#this is for the third set of filters: City, Stratum, Age:
#df_label_Fields_vis = pd.read_csv("data/lang/vis/option_fields_" + lang + ".csv", sep=",",encoding="latin1", skipinitialspace=True)
#option3_ddFields_vis = []
#for index, row in df_label_Fields_vis.iterrows():
#    option3_ddFields_vis.append( {'label': row['label'], 'value': row['field'] } )

#this is for the third set of filters: City, Sex(gender), Age, Stratum:
#this is just to know what function to use to get info from AWS:
# city for dataframeCiudades()
# sex/age/stratum for dataframeSexo_Edad_estrato()
option3_ddFields_vis = [
                        {'label': 'City', 'value': 'city'}, #this is just to know what function to use to get info from AWS
                        {'label': 'Sex (gender)', 'value': 'gender'}, #this is just to know what to put in the X-axis when plotting         
                        {'label': 'Age', 'value': 'age'}, #this is just to know what to put in the X-axis when plotting
                        {'label': 'Stratum', 'value': 'stratum'} #this is just to know what to put in the X-axis when plotting                  
                    ]

#here is the graph located...

#this is for the fourth set of filters: selecting each period with a slider
#Slider marks:
#to fix the slider steps from 12 to 60, with 25 steps spaced "2 units", thus resulting in this 25 prefixes: 12, 14, 16,...,56, 58, 60 
#as periods has 122009-01, so by subslicing [4:9] goes from the 4th to the 8th position to get the desired info as YY-PP format!
option4_slider_vis = {
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
#this is for the fifth set of filters: selecting gender (M/F) or ALL, i.e. ALL means aggregated and this works only for dataframeCiudades() 
#but the word 'gender' the groupby made (to be used: this works only for dataframeSexo_Edad_Estrato(dataset, ejeX, period, variable, gender); variable=['gender', 'age', 'stratum'] 
option5_radio_vis = [
                        {'label': 'All', 'value': 'ALL'}, #ALL(both)-by default
                        {'label': 'Women', 'value': 'F'},#Female
                        {'label': 'Men', 'value': 'M'},#Male
                    ]               
#STORING THE DEFAULT DF:
#def dataframeCiudades(dataset, ejeX, period, gender)
#dataframeCiudades('enrolled_uao','faculty','2017-01','M') #here period is fixed as well as sex/gender
#def update_graph(selected_dataset, selected_fac_program, selected_city_st_age, selected_period, selected_gender):# 5 options in total
#df = dataframeCiudades(selected_dataset, selected_fac_program, selected_period, selected_gender) #here period is fixed as well as sex/gender
#period = str(selected_period)[2:6] + '-' + str(selected_period)[6:8] # it is necesary to be used in the functions

'''
 default: PLOTTING 'conteo' in the Y-axis for a scatter quantity graph (conteo vs fac/prog)
 otherwise: PLOTTING 'another variable' in the Y-axis for a scatter/boxplot/violinplot distribution graph (var vs fac/prog)
'''
df = dataframeCiudades('enrolled_uao','faculty','ALL','ALL') #default
#print('df=',df)
#print('df.columns=',df.columns)

#fig_vis = px.scatter(df,x="facultad",y="conteo", color="ciudad") #default
#default: df.columns[0]="facultad"; df.columns[2]="conteo"; df.columns[1]="ciudad"
#fig_vis = px.bar(df,x=df.columns[0],y=df.columns[2], color=df.columns[1])# try changing px.bar / px.lineplot / px.boxplot? 

#fuction to be called:
def contentVisualization():
    #print('showing contentVisualization')
    return dbc.Collapse([
                            html.Br(),
                            html.H1("Visualization",id="titulo_visualization"),        
                            html.Hr(),
                            html.Div([
                                dbc.Row([
                                    dbc.Col(
                                        html.Div("Choose the desired database:", className="col-6" ),
                                    ),
                                    dbc.Col(
                                        html.Div("Select the type of plot:", className="col-6" ),
                                    ),
                                ]),                            

                                dbc.Row([
                                    dbc.Col(
                                        dcc.RadioItems(
                                            id='option1-radio-vis',#ids with hyphen to differiantiate them
                                            options=option1_radio_vis,
                                            value=datasets[0],#'enrolled_uao',
                                            labelStyle={'margin-left':'10px'}#to be separated among them
                                        ),
                                    ),
                                    dbc.Col(
                                        dcc.Dropdown(#selected_plot_type:'ycount'(for a quantity plot: count vs fac/prog); 'yother'(for a distribution plot: var vs fac/prog)
                                            id='option0-ddFields-vis', 
                                            options=option0_ddFields_vis, # ycount, yother
                                            value='ycount'
                                        ),
                                    ),
                                ]),                          
                            ]),
                            #html.Hr(),
                            html.Br(),
                            html.Div([
                                dbc.Row([
                                    dbc.Col(
                                        html.Div("Grouping option:", className="col-6"),
                                    ),
                                    dbc.Col(
                                        html.Div("Variable to graph:", className="col-6" ),
                                    ),
                                    dbc.Col(
                                        html.Div("Filter by Gender:", className="col-6" ),
                                    ),
                                ]),

                                dbc.Row([
                                    dbc.Col(
                                        dcc.RadioItems(
                                            id='option2-radio-vis',
                                            options=option2_radio_vis,
                                            value='faculty',
                                            labelStyle={'margin-left':'10px'}#to be separated among them
                                        ),                                    
                                    ),
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id='option3-ddFields-vis', #to differentiate from the above dropdown
                                            options=option3_ddFields_vis, # city, gender, age, stratum
                                            value='city'
                                        ),
                                    ),
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id = 'option5-radio-vis',
                                            options=option5_radio_vis,
                                            value='ALL', #default
                                            #labelStyle={'margin-left':'10px'},
                                            #className="col-6" #, this comma should not be here
                                        ),
                                    ),
                                ]),
                            ]),
                            #html.Hr(),
                            html.Br(),
                            html.Div([  
                                        
                                        #html.Div(
                                        #            "Use the slider to select the period (Year-Semester or All):",
                                        #             className="col-6"
                                        #        ),
                                        dcc.Slider(# in the callback, df must be the ddf
                                                    id = 'option4-slider-vis',
                                                    min = 12200901, #must be integer(YYYY0X), X={1,3} for 1st and 2nd semester (period)
                                                    max = 61202100, #then, for instance, it will be turn into "2020-03"              
                                                    step = None, #default one by one                                                                                                                                                           
                                                    marks=option4_slider_vis,
                                                    value= 61202100, #default('ALL')
                                                    included=False
                                                ),
                                        dcc.Graph(id='main-graph-vis'), # this graph updates automatically       
                                    ]),

                            #Optionally- showing the dataframe in a table:
                            html.Div([
                                        html.Div(
                                                    "Table:",
                                                    className="col-6"
                                                ),
                                    ], 
                                    className="row"),                                      
                            dash_table.DataTable(
                                                    id='table-vis',
                                                    data=df.to_dict('records'),
                                                    columns=[{'id': c, 'name': c} for c in df.columns],
                                                ),#this comma needs to be here
                            html.Hr(),                            
                        ],id="contentVisualization", className="container content", is_open=False) #className="content"
#Callback sets:
@app.callback(
                [dash.dependencies.Output('option3-ddFields-vis', 'value'),
                dash.dependencies.Output('option3-ddFields-vis', 'disabled'),
                ],
                [Input('option0-ddFields-vis', 'value'),#value0=plot-type (selected_plot_type)
                ]#in the order of the inputs, value represents the following argumnets of the update_graph fucntion:
            ) 

def update_variable(selected_plot_type):
    if selected_plot_type == 'yother':
        return 'age',True
    else:
        return 'city', False


@app.callback(
                [Output('main-graph-vis', 'figure'),    #graph                
                Output('table-vis', 'data'),            #table-data
                Output('table-vis', 'columns')          #table-columns
                ],
                [Input('option0-ddFields-vis', 'value'),#value0=plot-type (selected_plot_type)
                Input('option1-radio-vis', 'value'),    #value1=dataset (selected_dataset)
                Input('option2-radio-vis', 'value'),    #value2=program-faculty (selected_fac_program)
                Input('option3-ddFields-vis', 'value'), #value3=city-sex-age-stratum (selected_city_st_age)
                Input('option4-slider-vis', 'value'),   #value4=period (selected_period)                
                Input('option5-radio-vis', 'value')     #value6=men-women-all (selected_gender)                            
                ]#in the order of the inputs, value represents the folloeing argumnets of the update_graph fucntion:
            ) 

def update_graph(selected_plot_type, selected_dataset, selected_fac_program, selected_city_sex_age_st, selected_period, selected_gender):#5--- #selected_tperiod, selected_gender):# 6 options in total

    #print('updating graph...')                 
    if selected_period!=61202100:
        selected_period_str=str(selected_period)[2:6]+'-'+str(selected_period)[6:8]#slicing goes up to sup lim - 1
    else:
        selected_period_str = 'ALL'
    
    #initializing the first graph to show by default!!!
    #print('initializing the first graph to show by default...')
    df = dataframeCiudades(selected_dataset, selected_fac_program, selected_period_str, selected_gender) #here period is fixed as well as 

    #City is the default; if there is different variable our DataFrame will be built by the second function
    if selected_city_sex_age_st!='city':
        df = dataframeSexo_Edad_Estrato(selected_dataset, selected_fac_program, selected_period_str, selected_city_sex_age_st, selected_gender, selected_plot_type) #here period is fixed as well as sex/
    
    columns=[{"name": i, "id": i} for i in df.columns] #(*)
    data=df.to_dict('records') #df is going to be shown 

    if selected_plot_type=='ycount': #default
        #traces = getTraces(df,1,0,2,1)
        #return_slider_and_graph = get_slider_and_graph(df,traces,0,2)
        #fig_vis = px.scatter(df,x=df.columns[0],y=df.columns[2], color=df.columns[1])
        name = df.columns[1]
        df[name] = df[name].astype('category')
        fig_vis = px.bar(df,x=df.columns[0],y=df.columns[2], color=df.columns[1], barmode='group')
    else: #other variable ('yother')
        #traces = getTraces(df,2,0,1,2)
        fig_vis = px.box(df,x=df.columns[0],y=df.columns[1], 
             color_discrete_sequence=px.colors.diverging.RdYlBu)
    
    return fig_vis, data, columns  #fig_vis==return_slider (sliders updates the graph)

#------------------------------
#END OF contentVisualization.py
#------------------------------