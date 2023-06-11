import dash
from dash.dependencies import Input, Output
from dash import dash_table
from dash.dash_table.Format import Group
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from app import app

# =========  Layout  =========== #
layout = dbc.Col([
    dbc.Row([
        dbc.Col(
            dbc.Card(
                html.Legend('Extrato Completo'),
                # html.Div(
                #     id='tabela-geral',
                #     className='dbc'
                # )
            )
        )
    ],
        style={
            'height': '100%',
            'padding': '10px',
            'margin': '5px'
        }
    ),
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dcc.Graph(
                    id='graph-geral',
                    style={'margin': '20px'}
                )
            )
        )
    ], style={
        'height': '100%',
        'padding': '10px',
        'margin': '5px'}
    )
],
    style={
        'padding':
        '10px', 'margin':
        '5px'
    }
)

# =========  Callbacks  =========== #
# Tabela
