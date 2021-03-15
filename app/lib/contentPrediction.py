#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------
#Start of contentPrediction.py
#-----------------------------
#Libraries:
import pickle
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table
#from sklearn.linear_model import LogisticRegression
from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px
#this is required to be able to use callbacks inside every Python script:
from app import app
#--------------------------------

###################################################################################################################
##Connection to AWS RDS
host = '****'                   #AWS RDS instance
port = 5432                     #default port
user = '****'                   #database user
password = '****'               #database password
database = '****'               #database name
connDB = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}') #database connection (only once)
###################################################################################################################

cities = pd.read_sql('SELECT DISTINCT school_city, school_state FROM enrolled_uao ORDER BY school_city', connDB)

#useful to control the variables language (only one can be run (enabled) at a time)
lang='en' #default
#lang='sp'

#Defining the Prediction section:
#'foreign','age_range','civil_status','stratum','school_city','semester','faculty'
# foreign
# ['no' 'nd' 'si']
cols_foreign=[{'label': 'yes', 'value': 'si'},{'label': 'no', 'value': 'no'}]
# civil_status
# ['soltero' 'union libre' 'casado' 'separado' 'no definido' 'divorciado'
#  'viudo']
cols_civil_status=[{'label': 'Single', 'value': 'soltero'},
                    {'label': 'Free Union', 'value': 'union libre'},
                    {'label': 'Married', 'value': 'casado'},
                    {'label': 'Separated', 'value': 'separado'},
                    {'label': 'Undefined', 'value': 'no definido'},
                    {'label': 'Divorced', 'value': 'divorciado'},
                    {'label': 'Widower', 'value': 'viudo'}
                    ]
# stratum
# [3 4 5 2 6 1]
cols_stratum=[{'label': '1', 'value': '1'},
                {'label': '2', 'value': '2'},
                {'label': '3', 'value': '3'},
                {'label': '4', 'value': '4'},
                {'label': '5', 'value': '5'},
                {'label': '6', 'value': '6'}]

cols_school_city=[]
for _,row  in cities.iterrows():
    cols_school_city.append({'label': row['school_city'].capitalize() + ' - ' + row['school_state'].capitalize(), 'value': row['school_city']})

# semester
cols_semester=[{'label': '1', 'value': '1'}, {'label': '2', 'value': '2'}]

# faculty
cols_faculty=[{'label': 'Faculty of Administrative Sciences', 'value': 'facultad de ciencias administrativas' },
            {'label': 'Faculty of Communication and Social Sciences', 'value': 'facultad de comunicacion y ciencias sociales'},
            {'label': 'Faculty of Humanities and Arts', 'value': 'facultad de humanidades y artes' },
            {'label': 'Faculty of Engineering', 'value': 'facultad de ingenieria'}
]

#Defining the maon function:
def getMenuPredict():
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Row( dbc.Col( "Faculty")),
                dbc.Row(
                    dbc.Col(
                        dcc.Dropdown(
                            id='faculty-dropdown_predict',
                            options=cols_faculty,
                            value=cols_faculty[0]['value'],
                            clearable=False
                        )
                    )
                )
            ],md=6),
            dbc.Col([
                dbc.Row( dbc.Col("Semester" ) ),
                dbc.Row(
                    dbc.Col(
                        dcc.Dropdown(
                            id='semester-dropdown_predict',
                            options=cols_semester,
                            value=cols_semester[0]['value'],
                            clearable=False
                        )
                    )
                )
            ],md=6)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Row( dbc.Col( "School City")),
                dbc.Row(
                    dbc.Col(
                        dcc.Dropdown(
                            id='school_city-dropdown_predict',
                            options=cols_school_city,
                            value='cali',
                            #value=cols_school_city[0]['value'],
                            clearable=False
                        )
                    )
                )
            ],md=6),
            dbc.Col([
                dbc.Row( dbc.Col("Stratum" ) ),
                dbc.Row(
                    dbc.Col(
                        dcc.Dropdown(
                            id='stratum-dropdown_predict',
                            options=cols_stratum,
                            value=cols_stratum[0]['value'],
                            clearable=False
                        )
                    )
                )
            ],md=6)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Row( dbc.Col( "Civil status")),
                dbc.Row(
                    dbc.Col(
                        dcc.Dropdown(
                            id='civil_status-dropdown_predict',
                            options=cols_civil_status,
                            value=cols_civil_status[0]['value'],
                            clearable=False
                        )
                    )
                )
            ],md=6),
            dbc.Col([
                dbc.Row( dbc.Col("Foreign" ) ),
                dbc.Row(
                    dbc.Col(
                        dcc.Dropdown(
                            id='foreign-dropdown_predict',
                            options=cols_foreign,
                            value=cols_foreign[0]['value'],
                            clearable=False
                        )
                    )
                )
            ],md=6)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Row( dbc.Col( "Age")),
                dbc.Row(
                    dbc.Col(
                        dcc.Slider(
                            id = 'age-slider_predict',
                            min=15,
                            max=40,
                            value=18,
                            marks={
                                15: {'label': '<10'},
                                18: {'label': '18'},
                                21: {'label': '21'},
                                26: {'label': '26'},
                                31: {'label': '31'},
                                40: {'label': '100<'}
                            },
                            included=False
                        )  
                    )
                )
            ],md=6)
        ]),
        dbc.Row(dbc.Col(
            dbc.Button("Predict", id="button_predict",className="btn-outline-danger"),
            className="d-flex justify-content-center"
        )),
    ])

#Another important fuction for the prediction model:
def do_predict(foreign,age_range,civil_status,stratum,school_city,semester,faculty):
    cols_model = ['foreign_no', 'foreign_si', 'age_range_rango_2', 'age_range_rango_3', 'age_range_rango_4', 'age_range_rango_5', 'civil_status_divorciado', 'civil_status_no definido', 'civil_status_separado', 'civil_status_soltero', 'civil_status_union libre', 'civil_status_viudo', 'stratum_2', 'stratum_3', 'stratum_4', 'stratum_5', 'stratum_6', 'school_city_acevedo', 'school_city_aguazul', 'school_city_alban', 'school_city_aldana', 'school_city_algeciras', 'school_city_almaguer', 'school_city_alto baudo', 'school_city_amaga', 'school_city_ancuya', 'school_city_andalucia', 'school_city_anserma', 'school_city_ansermanuevo', 'school_city_arauca', 'school_city_arboleda', 'school_city_argelia', 'school_city_armenia', 'school_city_bagado', 'school_city_balboa', 'school_city_baranoa', 'school_city_barbacoas', 'school_city_barbosa', 'school_city_barrancabermeja', 'school_city_barranquilla', 'school_city_belen de los andaquies', 'school_city_bello', 'school_city_betulia', 'school_city_bogota', 'school_city_bolivar', 'school_city_braward country', 'school_city_bucaramanga', 'school_city_buenaventura', 'school_city_buenos aires', 'school_city_buesaco', 'school_city_buga', 'school_city_bugalagrande', 'school_city_caicedonia', 'school_city_cajamarca', 'school_city_cajibio', 'school_city_cajica', 'school_city_calarca', 'school_city_caldono', 'school_city_cali', 'school_city_caloto', 'school_city_candelaria', 'school_city_cantagallo', 'school_city_carmelo candelaria', 'school_city_carmen de apicala', 'school_city_cartagena', 'school_city_cartago', 'school_city_casanare', 'school_city_caucasia', 'school_city_cerete', 'school_city_chachagui', 'school_city_chaparral', 'school_city_charco narino', 'school_city_chia', 'school_city_chinchina', 'school_city_cienaga', 'school_city_circasia', 'school_city_ciudad de estados unidos', 'school_city_ciudad de mexico', 'school_city_ciudad de venezuela', 'school_city_ciudad extranjero', 'school_city_ciudad sin informacion', 'school_city_colon', 'school_city_condoto', 'school_city_corinto', 'school_city_corozal', 'school_city_costa rica', 'school_city_cota', 'school_city_cuaspud', 'school_city_cucaita', 'school_city_cucuta', 'school_city_cumaribo', 'school_city_cumbal', 'school_city_cumbitara', 'school_city_curillo', 'school_city_dagua', 'school_city_darien', 'school_city_don matias', 'school_city_dosquebradas', 'school_city_dpto extranjero', 'school_city_duitama', 'school_city_el aguila', 'school_city_el banco', 'school_city_el cairo', 'school_city_el cerrito', 'school_city_el charco', 'school_city_el dobio valle', 'school_city_el doncello', 'school_city_el dovio', 'school_city_el paujil', 'school_city_el penol', 'school_city_el placer cerrito', 'school_city_el rosario', 'school_city_el santuario', 'school_city_el tambo', 'school_city_elias', 'school_city_encino', 'school_city_enciso', 'school_city_envigado', 'school_city_espinal', 'school_city_facatativa', 'school_city_falan', 'school_city_filandia', 'school_city_florencia', 'school_city_florida', 'school_city_floridablanca', 'school_city_francisco pizarro', 'school_city_funes', 'school_city_funza', 'school_city_fusagasuga', 'school_city_gamarra', 'school_city_garzon', 'school_city_gigante', 'school_city_ginebra', 'school_city_girardot', 'school_city_gramalotenorte de santander', 'school_city_granada', 'school_city_guacari', 'school_city_guachene', 'school_city_guachucal', 'school_city_guadalajara de buga', 'school_city_guadalupe', 'school_city_guaduas', 'school_city_guaitarilla', 'school_city_gualmatan', 'school_city_guapi', 'school_city_guayaquil', 'school_city_ibague', 'school_city_iles', 'school_city_inza', 'school_city_ipiales', 'school_city_isnos', 'school_city_itagui', 'school_city_itsmina', 'school_city_jamundi', 'school_city_la apartada', 'school_city_la argentina', 'school_city_la argentina huila', 'school_city_la cruz', 'school_city_la cumbre', 'school_city_la dorada', 'school_city_la estrella', 'school_city_la florida', 'school_city_la llanada', 'school_city_la plata', 'school_city_la sierra', 'school_city_la tola', 'school_city_la union', 'school_city_la vega', 'school_city_la victoria', 'school_city_leiva', 'school_city_lerida', 'school_city_leticia', 'school_city_libano', 'school_city_lopez', 'school_city_lorica', 'school_city_los andes', 'school_city_los patios', 'school_city_magangue', 'school_city_maicao', 'school_city_mallama', 'school_city_manaure', 'school_city_manizales', 'school_city_manzanares', 'school_city_mariquita', 'school_city_marmato', 'school_city_medellin', 'school_city_mercaderes', 'school_city_miranda', 'school_city_mitu', 'school_city_mocoa', 'school_city_momil', 'school_city_montelibano', 'school_city_monteria', 'school_city_morales', 'school_city_mosquera', 'school_city_natagaima', 'school_city_nechi', 'school_city_neiva', 'school_city_nemocon', 'school_city_new yersey', 'school_city_new york', 'school_city_new york city', 'school_city_nilo', 'school_city_novita', 'school_city_olaya herrera', 'school_city_olaya herreranarino', 'school_city_oporapa', 'school_city_orito', 'school_city_padilla', 'school_city_paez', 'school_city_palestina', 'school_city_palmira', 'school_city_pasto', 'school_city_patia', 'school_city_paz de ariporo', 'school_city_pensilvania caldas', 'school_city_pereira', 'school_city_piedecuesta', 'school_city_piedras', 'school_city_piendamo', 'school_city_pitalito', 'school_city_placer', 'school_city_plato', 'school_city_policarpa', 'school_city_popayan', 'school_city_potosi', 'school_city_potrerito', 'school_city_pradera', 'school_city_pto tejada', 'school_city_puerres', 'school_city_puerto asis', 'school_city_puerto carreno', 'school_city_puerto colombia', 'school_city_puerto lopez', 'school_city_puerto rico', 'school_city_puerto salgar', 'school_city_puerto tejada', 'school_city_pupiales', 'school_city_purificacion', 'school_city_quibdo', 'school_city_quinchia', 'school_city_quipile', 'school_city_restrepo', 'school_city_retiro', 'school_city_ricaurte', 'school_city_riofrio', 'school_city_riohacha', 'school_city_rionegro', 'school_city_roberto payan', 'school_city_roldanillo', 'school_city_rosas', 'school_city_rozo', 'school_city_sabanalarga', 'school_city_saldana', 'school_city_salento', 'school_city_samaniego', 'school_city_san agustin', 'school_city_san andres', 'school_city_san andres sotavento', 'school_city_san bernardo', 'school_city_san francisco', 'school_city_san jose', 'school_city_san jose del guaviare', 'school_city_san jose del palmar', 'school_city_san lorenzo', 'school_city_san martin', 'school_city_san miguel', 'school_city_san pablo', 'school_city_san pedro', 'school_city_san pedro de cartago', 'school_city_san vicente', 'school_city_san vicente del caguan', 'school_city_sandona', 'school_city_santa barbara', 'school_city_santa marta', 'school_city_santa rosa de cabal', 'school_city_santana', 'school_city_santander de quilichao', 'school_city_saravena', 'school_city_sevilla', 'school_city_sibundoy', 'school_city_silvia', 'school_city_sincelejo', 'school_city_soacha', 'school_city_sogamoso', 'school_city_soledad', 'school_city_suarez', 'school_city_suaza', 'school_city_tabio', 'school_city_tado', 'school_city_tambo', 'school_city_tame', 'school_city_taminango', 'school_city_tarqui', 'school_city_tauramena', 'school_city_tesalia', 'school_city_tierralta', 'school_city_timana', 'school_city_timbio', 'school_city_timbiqui', 'school_city_toluviejo', 'school_city_toribio', 'school_city_toro', 'school_city_trinidad', 'school_city_trujillo', 'school_city_tulua', 'school_city_tumaco', 'school_city_tunja', 'school_city_tuquerres', 'school_city_turbaco', 'school_city_turbo', 'school_city_valle del guamuez', 'school_city_valledupar', 'school_city_venezuela', 'school_city_versalles', 'school_city_vijes', 'school_city_villa rica', 'school_city_villagarzon', 'school_city_villagorgona', 'school_city_villamaria', 'school_city_villanueva', 'school_city_villavicencio', 'school_city_west palm beach florida', 'school_city_yacuanquer', 'school_city_yopal', 'school_city_yotoco', 'school_city_yumbo', 'school_city_zarzal', 'school_city_zipaquira', 'semester_2', 'faculty_facultad de comunicacion y ciencias sociales', 'faculty_facultad de humanidades y artes', 'faculty_facultad de ingenieria']
    original_values=[]
    original_values.append( 'foreign_' + foreign )
    original_values.append( 'age_range_' + age_range )
    original_values.append( 'civil_status_' + civil_status )
    original_values.append( 'stratum_' + stratum )
    original_values.append( 'school_city_' + school_city )
    original_values.append( 'semester_' + semester )
    original_values.append( 'faculty_' + faculty )
    data=[]
    for col in cols_model:
        if col in original_values:
            data.append(1)
        else:
            data.append(0)
    
    path_file='data/model_predict_lr_202011.mlr'
    model_lr = pickle.load(open(path_file, 'rb'))
    prob = model_lr.predict_proba([data])[0]
    clase = model_lr.predict([data])
    return clase, prob[0], prob[1]

def get_age_range(a):
  if a<18:
    return 'rango_1'
  if a<21:
    return 'rango_2'
  if a<26:
    return 'rango_3'
  if a<31:
    return 'rango_4'
  return 'rango_5'

#main section to display:
def contentPrediction():
    return dbc.Collapse([
        html.Br(),
        html.H1("Prediction",id="titulo_prediction"),
        dbc.Row([
            dbc.Col(
                getMenuPredict(),
                className="p-3",
                style={"border":"2px firebrick solid", 'border-radius': '25px'},
                md=8
            ),
            dbc.Col(
                html.Div(id='result_predict', className="d-flex justify-content-center"),
                md=4
            )
        ]),
        html.Hr(), 
    ], id="contentPrediction", className="container content", is_open=False)


#Callbacks sets:
@app.callback(
    Output("result_predict", "children"),
    [Input("button_predict", "n_clicks")],
    [State('faculty-dropdown_predict','value'),
     State('semester-dropdown_predict','value'),
     State('school_city-dropdown_predict','value'),
     State('stratum-dropdown_predict','value'),
     State('civil_status-dropdown_predict','value'),
     State('foreign-dropdown_predict','value'),
     State('age-slider_predict','value')]
)
def on_button_click(n, faculty, semester, school_city, stratum, civil_status, foreign, age ):
    age_range = get_age_range(age)
    clase, prob_no, prob_yes = do_predict(foreign,age_range,civil_status,stratum,school_city,semester,faculty)
    str_prob_yes = '{:.1f}'.format(100*prob_yes)
    str_prob_no = '{:.1f}'.format(100*prob_no)
    lst_cont = []
    if clase:
        lst_cont.append(
            dbc.Row(
                dbc.Col(
                    html.H1("YES", className="text-center"),
                    style={'color': '#FFFFFF',
                        'border-top-left-radius': '25px',
                        'border-top-right-radius': '25px',
                        "border":"2px black solid",
                        'backgroundColor': 'rgb(57,142,231)'
                    }
                )
            )
        )
    else:
        lst_cont.append(
            dbc.Row(
                dbc.Col(
                    html.H1("NO", className="text-center"),
                    className="bg-danger",
                    style={'color': '#FFFFFF',
                        'border-top-left-radius': '25px',
                        'border-top-right-radius': '25px',
                        "border":"2px black solid"
                    }
                )
            )
        )

    bdy = html.Div(
        dbc.Row([
            dbc.Col( [html.H3("Yes", className="text-center" , style={'color': '#FFFFFF'}),
                    html.H5(str_prob_yes + " %",
                        className="text-center",
                        style={'color': '#FFFFFF'}
                    )
                ],
                style={'border-bottom-left-radius': '25px',
                    "border":"2px black solid",
                    'backgroundColor': 'rgb(57,142,231)'
                }
            ),
            dbc.Col([html.H3("No", className="text-center", style={'color': '#FFFFFF'} ),
                html.H5(str_prob_no + " %",
                    className="text-center",
                    style={'color': '#FFFFFF'}
                )
                ],
                style={'border-bottom-right-radius': '25px',
                    "border":"2px black solid"
                },
                className="bg-danger"
            )
        ])
    )
    lst_cont.append(bdy)
    component = html.Div(lst_cont,
            style={"width": "18rem",
                #"border":"2px black solid",
                #'border-radius': '25px'
            }
        )
    return component
#---------------------------
#End of contentPrediction.py
#---------------------------

