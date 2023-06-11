from datetime import datetime, timedelta
from dash import html, dcc
from dash.dependencies import Input, Output, State

import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
from globals import *
from app import *

graph_margin = dict(l=25, r=25, t=25, b=0)

# =========  Layout  =========== #
layout = dbc.Col([
    dbc.Row([
        dbc.Col([
            #Filtragem do período de analise
            dbc.Card([
                html.Legend(
                    'Filtrar de Categorias',
                    className='card-title',
                    style={
                        'width': '100%',
                        'margin-bottom': '20px',
                        'text-align': 'center'
                    }
                ),
                html.Label(
                    'Categorias das Receitas',
                    style={
                        'width': '98%',
                        'margin-left': '5px',
                        'margin-right': '10px',
                    }
                ),
                html.Div(
                    dcc.Dropdown(
                        id='dropdown-receita',
                        clearable=False,
                        persistence=True,
                        persistence_type='session',
                        multi=True,
                        style={
                            'width': '98%',
                            'margin-left': '5px',
                            'margin-right': '10px',
                            'margin-top': '5px',
                            'margin-bottom': '20px',
                        }
                    )
                ),
                html.Label(
                    'Categorias das Despesas',
                    style={
                        'width': '98%',
                        'margin-left': '5px',
                        'margin-right': '10px',
                    }
                ),
                html.Div(
                    dcc.Dropdown(
                        id='dropdown-despesa',
                        clearable=False,
                        persistence=True,
                        persistence_type='session',
                        multi=True,
                        style={
                            'width': '98%',
                            'margin-left': '5px',
                            'margin-right': '10px',
                            'margin-top': '5px',
                            'margin-bottom': '20px',
                        }
                    )
                ),
                html.Legend(
                    'Periodo de Análise',
                    style={
                        'width': '100%',
                        'margin-bottom': '20px',
                        'text-align': 'center'
                    }
                ),
                dcc.DatePickerRange(
                    month_format='DD MMM, YY',
                    end_date_placeholder_text='Data...',
                    start_date=datetime(2023, 1, 1).date(),
                    end_date=datetime.today() + timedelta(days=31),
                    display_format='DD / MM / YYYY',
                    updatemode='singledate',
                    id='date-picker-config',
                    style={
                        'z-index': '100',
                            'width': '60%',
                            'margin-left': 'auto',
                            'margin-right': 'auto',
                            'margin-top': '5px',
                            'margin-bottom': '20px',
                    }
                )
            ], style={
                'height': '100%',
                'margin-bottom': '20px'
            })
        ],
            width=4,
            style={
                'margin-top': '10px',
            }
        ),
        dbc.Col([
            dbc.Card(
                dcc.Graph(id='graph1'),
            )
        ], 
        width=8,
        style={
            'margin-top': '10px', 
            'height': '100%'
        }
        )
    ], style={'margin': '10px'}),
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dcc.Graph(id='graph2'),
                style={'padding': '10px'}
            ), width=6
        ),
        dbc.Col(
            dbc.Card(
                dcc.Graph(id='graph3'),
                style={'padding': '10px'}
            ), width=3
        ),
        dbc.Col(
            dbc.Card(
                dcc.Graph(id='graph4'),
                style={'padding': '10px'}
            ), width=3
        ),
    ])
])


# =========  Callbacks  =========== #
# Filtragem das Categorias de Receitas Inclusas
@app.callback(
    [
        Output('dropdown-receita', 'options'),
        Output('dropdown-receita', 'value'),
    ],
    Input('store-receitas', 'data')
)
def receita_dropdown(dict_receitas):
    df_receita = pd.DataFrame(dict_receitas)
    receita_categorias = df_receita.Categoria.unique().tolist()
    receita_categorias_unique = [{'label': i, 'value': i} for i in receita_categorias]
    return (receita_categorias_unique, receita_categorias)

# Filtragem das Categorias de Despesas Inclusas
@app.callback(
    [
        Output('dropdown-despesa', 'options'),
        Output('dropdown-despesa', 'value'),
    ],
    Input('store-despesas', 'data')
)
def despesa_dropdown(dict_despesa):
    df_despesa = pd.DataFrame(dict_despesa)
    despesa_categorias = df_despesa.Categoria.unique().tolist()
    despesa_categorias_unique = [{'label': i, 'value': i} for i in despesa_categorias]
    return (despesa_categorias_unique, despesa_categorias)

# Grafico 01 - Analise dos Ganhos ao longo do Tempo
@app.callback(
    Output('graph1', 'figure'),
    [
        Input('store-despesas', 'data'),
        Input('store-receitas', 'data'),
        Input('dropdown-despesa', 'value'),
        Input('dropdown-receita', 'values')
    ]
)
def graph1(dict_despesas, dict_receitas, cat_despesa, cat_receita):
    df_despesas = pd.DataFrame(dict_despesas).set_index('Data')[['Valor']]
    df_receitas = pd.DataFrame(dict_receitas).set_index('Data')[['Valor']]
    df_gb_despesa = df_despesas.groupby('Data').sum().rename(columns={'Valor': 'Despesa'})
    df_gb_receita = df_receitas.groupby('Data').sum().rename(columns={'Valor': 'Receita'})
    df_acumulado = df_gb_despesa.join(df_gb_receita,how="outer").fillna(0)
    df_acumulado['Acumulado'] = df_acumulado['Receita'] - df_acumulado['Despesa']
    df_acumulado['Acumulado'] = df_acumulado['Acumulado'].cumsum()
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            name="Fluxo de caixa", 
            x=df_acumulado.index, 
            y=df_acumulado['Acumulado'], 
            mode='lines'
        )
    )
    fig.update_layout(margin=graph_margin)
    fig.update_layout(title={'text': 'Receita ao longo do Tempo'})
    #fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

#Grafico 02 - Analise das Categorias de Receita e Despesas
@app.callback(
    Output('graph2', 'figure'),
    [
        Input('store-receitas', 'data'),
        Input('store-despesas', 'data'),
        Input('dropdown-receita', 'value'),
        Input('dropdown-despesa', 'value'),
        Input('date-picker-config', 'start_date'),
        Input('date-picker-config', 'end_date')
    ]
)

def graph2(dict_despesas, dict_receitas, cat_despesa, cat_receita, start_date, end_date):
    df_receitas = pd.DataFrame(dict_receitas)
    df_despesas = pd.DataFrame(dict_despesas)

    df_despesas['Output'] = 'Despesas'
    df_receitas['Output'] = 'Receitas'
    df_concatenado = pd.concat([df_despesas, df_receitas])
    df_concatenado['Data'] = pd.to_datetime(df_concatenado['Data'])

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_concatenado = df_concatenado[
        (df_concatenado['Data'] >= start_date) &
        (df_concatenado['Data'] <= end_date)
    ]
    df_concatenado = df_concatenado[
        (df_concatenado['Categoria'].isin(cat_receita)) |
        (df_concatenado['Categoria'].isin(cat_despesa))
    ]

    fig = px.bar(df_concatenado, x='Data', y='Valor', color='Output', barmode='group')
    fig.update_layout(title={'text': 'Despesas X Receitas'})
    fig.update_layout(margin=graph_margin)
    #fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

@app.callback(
    Output('graph3', 'figure'),
    [
        Input('store-receitas', 'data'),
        Input('dropdown-receita', 'value'),
    ]
)

def pizza_receita(dict_receita, cat_receita):
    df_receitas = pd.DataFrame(dict_receita)
    df_receitas = df_receitas[df_receitas['Categoria'].isin(cat_receita)]

    fig = px.pie(df_receitas, values=df_receitas.Valor, names=df_receitas.Categoria, hole=.2)
    fig.update_layout(title={'text': 'Receitas'})
    fig.update_layout(margin=graph_margin)
    return fig

@app.callback(
    Output('graph4', 'figure'),
    [
        Input('store-despesas', 'data'),
        Input('dropdown-despesa', 'value'),
    ]
)

def pizza_despesa(dict_despesa, cat_despesa):
    df_despesas = pd.DataFrame(dict_despesa)
    df_despesas = df_despesas[df_despesas['Categoria'].isin(cat_despesa)]

    fig = px.pie(df_despesas, values=df_despesas.Valor, names=df_despesas.Categoria, hole=.2)
    fig.update_layout(title={'text': 'Despesas'})
    fig.update_layout(margin=graph_margin)
    return fig