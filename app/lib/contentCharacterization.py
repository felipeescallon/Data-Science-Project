#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------
#Start of contentCharacterization.py
#-----------------------------------

# Import libraries
import math
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash_table.Format import Format, Scheme, Sign, Symbol
from dash.dependencies import Input, Output, State

from sqlalchemy import create_engine
import pandas as pd
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

#Getting information:
def getData_to_DB_charact( source ):
    global rules
    rules = pd.read_sql("SELECT support, confidence, lift, leverage, conviction, antecedents, consequents, len_antecedents, len_consequents FROM rules WHERE len_antecedents>=2 AND len_consequents>=2 AND src='"+ source +"'", connDB)
    rules['items'] = rules[['antecedents', 'consequents']].apply(lambda x: x['antecedents']+':'+x['consequents'],axis=1 )
    rules['icon_antecedents'] = rules['antecedents'].apply(lambda x: ','.join([ dexplain_Fields[y]['emoji'] for y in x.split(':')]) )
    #rules['icon_antecedents'] = rules['antecedents'].apply(lambda x: ','.join([ emojis[y] for y in x.split(':')]) )
    rules['icon_consequents'] = rules['consequents'].apply(lambda x: ','.join([ dexplain_Fields[y]['emoji'] for y in x.split(':')]) )


#fuctions definition set:
def getProgramFaculty_charact():
    global rules

    lst_fac_prog=[ {'label': 'All', 'value': state_comp_charact['fac_prog'] } ]
    lst_age_fields=[ {'label': 'All', 'value': state_comp_charact['age'] } ]
    lst_stratum_fields=[ {'label': 'All', 'value': state_comp_charact['stratum'] } ]
    lst_knowledge_fields=[ {'label': 'All', 'value': state_comp_charact['knowledge'] } ]
    lst_enrolled_fields=[ {'label': 'All', 'value': state_comp_charact['enrolled'] } ]
    lst_gender_fields=[ {'label': 'All', 'value': state_comp_charact['gender'] } ]
    lst_calendar_fields=[ {'label': 'All', 'value': state_comp_charact['calendar'] } ]
    lst_school_sp_fields=[ {'label': 'All', 'value': state_comp_charact['school_sp'] } ]
    lst_semester_fields=[ {'label': 'All', 'value': state_comp_charact['semester'] } ]
    lst_shift_fields=[ {'label': 'All', 'value': state_comp_charact['shift'] } ]
    lst_others_fields = [{'label': 'All', 'value': state_comp_charact['other_field'] }]
    for campo in dexplain_Fields.keys():
        if campo.startswith('faculty_') or campo.startswith('program_'):
            if not campo in lst_fac_prog:
                lst_fac_prog.append( {'label': dexplain_Fields[campo]['lang'], 'value': campo } )
        elif campo.startswith('age_range_'):
            if not campo in lst_age_fields:
                lst_age_fields.append( {'label': dexplain_Fields[campo]['lang'], 'value': campo } )
        elif campo.startswith('stratum_'):
            if not campo in lst_stratum_fields:
                lst_stratum_fields.append( {'label': dexplain_Fields[campo]['lang'], 'value': campo } )
        elif campo.startswith('knowledge_area_'):
            if not campo in lst_knowledge_fields:
                lst_knowledge_fields.append( {'label': dexplain_Fields[campo]['lang'], 'value': campo } )
        elif campo.startswith('enrolled_'):
            if not campo in lst_enrolled_fields:
                lst_enrolled_fields.append( {'label': dexplain_Fields[campo]['lang'], 'value': campo } )
        elif campo.startswith('gender_'):
            if not campo in lst_gender_fields:
                lst_gender_fields.append( {'label': dexplain_Fields[campo]['lang'], 'value': campo } )
        elif campo.startswith('school_calendar_'):
            if not campo in lst_calendar_fields:
                lst_calendar_fields.append( {'label': dexplain_Fields[campo]['lang'], 'value': campo } )
        elif campo.startswith('school_spanish_'):
            if not campo in lst_school_sp_fields:
                lst_school_sp_fields.append( {'label': dexplain_Fields[campo]['lang'], 'value': campo } )
        elif campo.startswith('semester_'):
            if not campo in lst_semester_fields:
                lst_semester_fields.append( {'label': dexplain_Fields[campo]['lang'], 'value': campo } )
        elif campo.startswith('shift_'):
            if not campo in lst_shift_fields:
                lst_shift_fields.append( {'label': dexplain_Fields[campo]['lang'], 'value': campo } )
        else:
            if not campo in lst_others_fields:
                lst_others_fields.append( {'label': dexplain_Fields[campo]['lang'], 'value': campo } )

    #return (sorted(lst_fac_prog), sorted(lst_others_fields))
    
    return ( lst_fac_prog, lst_age_fields, lst_stratum_fields, lst_knowledge_fields, lst_enrolled_fields, lst_gender_fields, lst_calendar_fields, lst_school_sp_fields, lst_semester_fields, lst_shift_fields, lst_others_fields )



def filter_rules_charact( fac_prog, age, stratum, enrolled, gender, calendar, school_sp, semester, shift, field ):
    global rules_show, rules
    rules_show = rules.sort_values(['len_antecedents', 'len_consequents'], ascending=[False, False])
    
    if fac_prog != 'all':
        rules_show = rules_show[rules_show['items'].str.contains(fac_prog)]

    if age != 'all':
        rules_show = rules_show[rules_show['items'].str.contains(age)]

    if stratum != 'all':
        rules_show = rules_show[rules_show['items'].str.contains(stratum)]
    if enrolled != 'all':
        rules_show = rules_show[rules_show['items'].str.contains(enrolled)]
    if gender != 'all':
        rules_show = rules_show[rules_show['items'].str.contains(gender)]
    if calendar != 'all':
        rules_show = rules_show[rules_show['items'].str.contains(calendar)]
    if school_sp != 'all':
        rules_show = rules_show[rules_show['items'].str.contains(school_sp)]
    if semester != 'all':
        rules_show = rules_show[rules_show['items'].str.contains(semester)]
    if shift != 'all':
        rules_show = rules_show[rules_show['items'].str.contains(shift)]
    if field != 'all':
        rules_show = rules_show[rules_show['items'].str.contains(field)]

    rules_show.reset_index(inplace = True, drop=True)


def getConventions():
    lst_campos = list(dexplain_Fields.keys())
    n_items= len(lst_campos)
    limit = math.ceil(n_items/2.0)
    opc_left = []
    for i in range(limit,):
        campo = lst_campos[i]
        opc_left.append( dbc.NavItem( dexplain_Fields[campo]['emoji'] + ":" + dexplain_Fields[campo]['lang']) )

    opc_right = []
    for i in range(limit,n_items):
        campo = lst_campos[i]
        opc_right.append( dbc.NavItem( dexplain_Fields[campo]['emoji'] + ":" + dexplain_Fields[campo]['lang']) )
    return dbc.Row([
        dbc.Col(
            dbc.Nav(opc_left,vertical="md")
        ,md=6),
        dbc.Col(
            dbc.Nav(opc_right,vertical="md")
        ,md=6,)
    ],style={"border":"2px lightgray solid"})

def show_rule_charact(indx):
    if indx==-2:
        component = html.Div("No rules found.")
    elif indx==-1:
        component = html.Div("Select any rule to show more information.")
    else:
        row = rules_show.iloc[indx][['support', 'confidence', 'lift', 'leverage', 'conviction', 'antecedents', 'consequents']]
        lst_ant = []
        for ant in row['antecedents'].split(':'):
            lst_ant.append(dbc.ListGroupItem( dexplain_Fields[ant]['lang']  ))
        lst_cons = []
        for cons in row['consequents'].split(':'):
            lst_cons.append(dbc.ListGroupItem( dexplain_Fields[cons]['lang'] ))

        conf = '{:.2f}'.format(100*row['confidence'])
        lift = '{:.2f}'.format(row['lift'])
        component = html.Div([
            dbc.Row( dbc.Col( "Students with the following characteristics")),
            dbc.Row( dbc.Col( dbc.ListGroup(lst_ant) ,md=12)),
            dbc.Row( dbc.Col( "Imply")),
            dbc.Row( dbc.Col( dbc.ListGroup(lst_cons) ,md=12)),
            dbc.Row( dbc.Col( "With")),
            html.Div([
                dbc.Row([
                    dbc.Col( "Confidence", md=6),
                    dbc.Col( conf + " %" ,md=6 )
                ]),
                dbc.Row([ 
                    dbc.Col( "Lift",md=6),
                    dbc.Col( lift ,md=6)
                ])
            ], className="container"),
        ])
    return component

#Stating components to be displayed:
state_comp_charact ={
    #'database':'enrolled',
    'database':'registered',
    'fac_prog':'all',
    'age':'all',
    'stratum':'all',
    'knowledge':'all',
    'enrolled':'all',
    'gender':'all',
    'calendar':'all',
    'school_sp':'all',
    'semester':'all',
    'shift':'all',
    'other_field':'all',
    'index_rule':-1
}

option1_radio_charact = [
                        {'label': "Enrolled",   'value': 'enrolled'},#df0='enrolled_uao'
                        {'label': 'Registered', 'value': 'registered'},#df1='registered_uao'
                        {'label': 'Deserters',  'value': 'deserters'} #df2='deserters_uao'
                    ]

df_explain_Fields = pd.read_csv("data/lang/characterization_fields_sp.csv", sep=",", encoding='utf8', skipinitialspace=True)
dexplain_Fields = {d['campo'].strip(): {'lang':d['en'].strip(),'emoji':d['emoji'].strip()} for d in df_explain_Fields.to_dict(orient='records')}

cols_show = ['icon_antecedents', 'icon_consequents']
#cols_show = ['antecedents', 'consequents']

rules = None
rules_show = None




#Main fuction:
def contentCharacterization():
    #getData_to_DB('registered')
    getData_to_DB_charact(state_comp_charact['database'])
    filter_rules_charact('all','all','all','all','all','all', 'all', 'all', 'all', 'all')
    (option_fac_prog,age_fields,stratum_fields,knowledge_fields, 
    enrolled_fields, gender_fields, calendar_fields, school_sp_fields, semester_fields, shift_fields,
    option_others_fields) = getProgramFaculty_charact()

    return dbc.Collapse([
        html.Br(),
        html.H1("Characterization",id="titulo_characterization"),
        html.Hr(),
        #html.H6("Caracterización"),
        dbc.Row( dbc.Col("Choose the desired database:" ) ),
        dbc.Row( dbc.Col(
            dcc.RadioItems(
                id='option1-radio-charact',#ids with hyphen to differiantiate them
                options=option1_radio_charact,
                value=state_comp_charact['database'],
                labelStyle={'margin-left':'10px'}
            )
        ) ),
        dbc.Row([
            dbc.Col([
                dbc.Row( dbc.Col( "Faculty or program")),
                dbc.Row(
                    dbc.Col(
                        dcc.Dropdown(
                            id='fac_prog-dropdown_charact',
                            options=option_fac_prog,
                            value=state_comp_charact['fac_prog'],
                            clearable=False
                        )
                    )
                )
            ],md=6),
            dbc.Col([
                dbc.Row( dbc.Col("Age" ) ),
                dbc.Row(
                    dbc.Col(
                        dcc.Dropdown(
                            id='age-dropdown_charact',
                            options=age_fields,
                            value=state_comp_charact['age'],
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
                            id='stratum-dropdown_charact',
                            options=stratum_fields,
                            value=state_comp_charact['stratum'],
                            clearable=False
                        )
                    )
                )
            ],md=6),
            # dbc.Col([
            #     dbc.Row( dbc.Col("Knowledge area" ) ),
            #     dbc.Row(
            #         dbc.Col(
            #             dcc.Dropdown(
            #                 id='knowledge-dropdown_charact',
            #                 options=knowledge_fields,
            #                 value=state_comp_charact['knowledge'],
            #                 clearable=False
            #             )
            #         )
            #     )
            # ],md=6),
            dbc.Col([
                dbc.Row( dbc.Col("Enrolled" ) ),
                dbc.Row(
                    dbc.Col(
                        dcc.Dropdown(
                            id='enrolled-dropdown_charact',
                            options=enrolled_fields,
                            value=state_comp_charact['enrolled'],
                            clearable=False
                        )
                    )
                )
            ],md=6),
            dbc.Col([
                dbc.Row( dbc.Col("Gender" ) ),
                dbc.Row(
                    dbc.Col(
                        dcc.Dropdown(
                            id='gender-dropdown_charact',
                            options=gender_fields,
                            value=state_comp_charact['gender'],
                            clearable=False
                        )
                    )
                )
            ],md=6),
            dbc.Col([
                dbc.Row( dbc.Col("School calendar" ) ),
                dbc.Row(
                    dbc.Col(
                        dcc.Dropdown(
                            id='calendar-dropdown_charact',
                            options=calendar_fields,
                            value=state_comp_charact['calendar'],
                            clearable=False
                        )
                    )
                )
            ],md=6),
            dbc.Col([
                dbc.Row( dbc.Col("School language" ) ),
                dbc.Row(
                    dbc.Col(
                        dcc.Dropdown(
                            id='school_sp-dropdown_charact',
                            options=school_sp_fields,
                            value=state_comp_charact['school_sp'],
                            clearable=False
                        )
                    )
                )
            ],md=6),
            dbc.Col([
                dbc.Row( dbc.Col("Registration Semester" ) ),
                dbc.Row(
                    dbc.Col(
                        dcc.Dropdown(
                            id='semester-dropdown_charact',
                            options=semester_fields,
                            value=state_comp_charact['semester'],
                            clearable=False
                        )
                    )
                )
            ],md=6),
            dbc.Col([
                dbc.Row( dbc.Col( "School shift" ) ),
                dbc.Row(
                    dbc.Col(
                        dcc.Dropdown(
                            id='shift-dropdown_charact',
                            options=shift_fields,
                            value=state_comp_charact['shift'],
                            clearable=False
                        )
                    )
                )
            ],md=6),
            dbc.Col([
                dbc.Row( dbc.Col("Other fields" ) ),
                dbc.Row(
                    dbc.Col(
                        dcc.Dropdown(
                            id='others_fields-dropdown_charact',
                            options=option_others_fields,
                            value=state_comp_charact['other_field'],
                            clearable=False
                        )
                    )
                )
            ],md=6),
        ]),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dash_table.DataTable(
                    id='table_rules_charact',
                    columns=[{'name': 'Antecedents',
                            'id': 'icon_antecedents',
                            'type': 'text'
                            },
                            {'name': 'Consequents',
                            'id': 'icon_consequents',
                            'type': 'text'
                            },
                            #{'name': 'Confidence',
                            #'id': 'confidence',
                            #'type': 'numeric',
                            #'format': Format(
                            #      precision=3,
                            #      #scheme=Scheme.fixed,
                            #      #symbol=Symbol.yes,
                            #      #symbol_suffix=u'˚F'
                            #  )
                            #}
                    ],
                    data=rules_show[cols_show].to_dict('records'),
                    row_selectable='single',
                    selected_rows=[],
                    style_as_list_view=True,
                    page_size=10,
                    style_data_conditional=[{
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(225,238,244)'
                    }],
                    style_header={
                        'backgroundColor': 'rgb(178, 34, 34)',
                        'fontWeight': 'bold',
                        'textAlign': 'left',
                        'color': 'white'
                    },
                    style_cell={
                        'border': '1px solid grey',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        'maxWidth': 0,
                        'textAlign': 'left',
                        'fontSize':18
                    },
                ),
                html.Div([
                    dbc.Button([
                        "Conventions",
                        html.I(className="fas fa-caret-down")
                        ],
                        id="det_convention-button_charact",
                        color="secondary", block=True,
                        style={'height': '19px', 'padding': '0'},
                        className="text-left"
                    ),
                    dbc.Fade(
                        getConventions(),
                        id="det_convention_charact",
                        is_in=False,
                        appear=False,
                    ),
                    ],style={'marginBottom': 50, 'marginTop': 50})
            ],md="8"),
            dbc.Col(
                html.Div(id='detail_rule_charact', className="container", style={"border":"2px firebrick solid", 'border-radius': '25px'})
            ,md="4")
        ]),
        html.Hr(),
        html.Hr(),
    ], id="contentCharacterization", className="container content", is_open=False)  # non-default page

#Necessary event to show/hide the conventions for the emojis used in this section of the application (Callback setting):
@app.callback(
    Output("det_convention_charact", "is_in"),
    [Input("det_convention-button_charact", "n_clicks")],
    [State("det_convention_charact", "is_in")],
)
def toggle_fade(n, is_in):
    if not n:
        # Button has never been clicked
        return False
    return not is_in



@app.callback([Output('fac_prog-dropdown_charact','value'),
    Output('age-dropdown_charact', 'value'),
    Output('stratum-dropdown_charact', 'value'),
    Output('enrolled-dropdown_charact', 'value'),
    Output('gender-dropdown_charact', 'value'),
    Output('calendar-dropdown_charact', 'value'),
    Output('school_sp-dropdown_charact', 'value'),
    Output('semester-dropdown_charact', 'value'),
    Output('shift-dropdown_charact', 'value'),
    Output('others_fields-dropdown_charact', 'value'),
    ],
    [Input('option1-radio-charact', 'value')])
def change_DB_charact( db ):
    fac_prog = state_comp_charact['fac_prog']
    age = state_comp_charact['age']
    stratum = state_comp_charact['stratum']
    enrolled = state_comp_charact['enrolled']
    gender = state_comp_charact['gender']
    calendar = state_comp_charact['calendar']
    school_sp = state_comp_charact['school_sp']
    semester = state_comp_charact['semester']
    shift = state_comp_charact['shift']
    other_field = state_comp_charact['other_field']

    if db != state_comp_charact['database']:
        getData_to_DB_charact( db )
        state_comp_charact['database'] = db
        state_comp_charact['fac_prog'] = '-1'
        fac_prog = 'all'
        age = 'all'
        stratum = 'all'
        enrolled = 'all'
        gender = 'all'
        calendar = 'all'
        school_sp = 'all'
        semester = 'all'
        shift = 'all'
        other_field = 'all'
    
    return fac_prog, age, stratum, enrolled, gender, calendar, school_sp, semester, shift, other_field


@app.callback([Output('table_rules_charact', 'data'),
    Output('table_rules_charact', 'selected_rows')],
    [Input('fac_prog-dropdown_charact', 'value'),
    Input('age-dropdown_charact', 'value'),
    Input('stratum-dropdown_charact', 'value'),
    Input('enrolled-dropdown_charact', 'value'),
    Input('gender-dropdown_charact', 'value'),
    Input('calendar-dropdown_charact', 'value'),
    Input('school_sp-dropdown_charact', 'value'),
    Input('semester-dropdown_charact', 'value'),
    Input('shift-dropdown_charact', 'value'),
    Input('others_fields-dropdown_charact', 'value')],
    [State('table_rules_charact','selected_rows')])
def update_rules_charact( fac_prog_field,age,stratum,enrolled, gender, calendar, school_sp, semester, shift,others_fields, selected_row_indices):
    global state_comp_charact
    #state_comp_charact['enrolled'], state_comp_charact['gender'], state_comp_charact['calendar']
    #state_comp_charact['school_sp'], state_comp_charact['semester'], state_comp_charact['shift']

    if (state_comp_charact['fac_prog'] != fac_prog_field or
            state_comp_charact['age'] != age or
            state_comp_charact['stratum'] != stratum or
            state_comp_charact['enrolled'] != enrolled or
            state_comp_charact['gender'] != gender or
            state_comp_charact['calendar'] != calendar or
            state_comp_charact['school_sp'] != school_sp or
            state_comp_charact['semester'] != semester or
            state_comp_charact['shift'] != shift or
            state_comp_charact['other_field'] != others_fields):
        filter_rules_charact( fac_prog_field, age, stratum, enrolled, gender, calendar, school_sp, semester, shift, others_fields )
        state_comp_charact['fac_prog'] = fac_prog_field
        state_comp_charact['age'] = age
        state_comp_charact['stratum'] = stratum
        state_comp_charact['enrolled'] = enrolled
        state_comp_charact['gender'] = gender
        state_comp_charact['calendar'] = calendar
        state_comp_charact['school_sp'] = school_sp
        state_comp_charact['semester'] = semester
        state_comp_charact['shift'] = shift
        state_comp_charact['other_field'] = others_fields
        if len(rules_show)==0:
            selected_row_indices=[-2]
        else:
            selected_row_indices=[-1]
        state_comp_charact['index_rule'] = -2

    data=rules_show[cols_show].to_dict('records')
    return data,selected_row_indices


@app.callback(Output('detail_rule_charact','children'),
    [Input('table_rules_charact', 'selected_rows')])
def showDet_rules_charact( selected_row_indices):
    global state_comp_charact
    
    component = show_rule_charact(-1)
    if len(selected_row_indices) == 0:
        if state_comp_charact['index_rule'] == -2:
            component = show_rule_charact(-2)
        elif state_comp_charact['index_rule'] != -1:
            component = show_rule_charact(-1)

        state_comp_charact['index_rule'] = -1
    else:
        i = selected_row_indices[0]
        if i<0:
            component = show_rule_charact(i)
        elif i != state_comp_charact['index_rule']:
            component = show_rule_charact(i)
            state_comp_charact['index_rule'] = i

    return component








#---------------------------------
#End of contentCharacterization.py
#---------------------------------    