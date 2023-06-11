import dash
from dash.dependencies import Input, Output
from dash import dash_table
from dash.dash_table.Format import Group
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

from app import app

# =========  Layout  =========== #
layout = dbc.Col([
    dbc.Row([
        dbc.Col(
            html.Legend('Filtra Contas: '),
            style={
            },
            width=2
        ),
        dbc.Col(
            html.Div(
                dcc.Dropdown(
                    id='dropdown-contas-despesas',
                    clearable=False,
                    persistence=True,
                    persistence_type='session',
                    multi=True,
                )
            ), 
            style={
                'width': '30%',
                'margin-right': '10px'
            },
            width=4
        ),
    ], style={
        'margin-top': '10px'
    }),
    dbc.Row([
        dbc.Col(
            dbc.Card(
                html.Div(
                    id="tabela-despesas",
                    className="dbc"
                )
            )
        )
    ], style={
        'height': '100%',
        'padding': '10px',
        'margin': '5px',
    }
    ),
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dcc.Graph(
                    id='graph-despesas',
                    style={'margin': '20px'}
                )
            )
        )
    ], style={
        'height': '100%',
        'padding': '10px',
        'margin': '5px'}
    )
])


# =========  Callbacks  =========== #
# Dropdown - Lista de Conta
@app.callback(
    [
        Output('dropdown-contas-despesas', 'options'),
        Output('dropdown-contas-despesas', 'value'),
    ],
    Input('store-despesas', 'data')
)
def conta_dropdown(dict_despesa):
    df_despesa = pd.DataFrame(dict_despesa)
    despesa_conta = df_despesa.Conta.unique().tolist()
    despesa_conta_unique = [{'label': i, 'value': i} for i in despesa_conta]
    return (despesa_conta_unique, despesa_conta)

# Tabela Despesas
@app.callback(
    Output('tabela-despesas', 'children'),
    [
        Input('store-despesas', 'data'),
        Input('dropdown-contas-despesas', 'value'),

    ]
)
def tabela_despesas (dict_despesas, contas):
    df = pd.DataFrame(dict_despesas)
    df['Data'] = pd.to_datetime(df['Data']).dt.date

    df = df.drop(columns=['Usuario'])

    df = df.fillna('-')

    df.loc[df['Efetuado'] == 0, 'Efetuado'] = 'Não'
    df.loc[df['Efetuado'] == 1, 'Efetuado'] = 'Sim'

    df.loc[df['Recorrente'] == 0, 'Recorrente'] = 'Não'
    df.loc[df['Recorrente'] == 1, 'Recorrente'] = 'Sim'

    df.sort_values(by='Data', ascending=True)


    df = df[(df['Conta'].isin(contas))]

    tabela = dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": True}
            if i == "Descrição" or i == "Fixo" or i == "Efetuado"
            else {"name": i, "id": i, "deletable": False, "selectable": False}
            for i in df.columns
        ],

        data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode="single",
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
    ),
    return tabela

# Bar Graph            
@app.callback(
    Output('graph-despesas', 'figure'),
    Input('store-despesas', 'data'),
)
def bar_chart(data):
    df = pd.DataFrame(data)
    df_grouped = df.groupby("Categoria").sum()[["Valor"]].reset_index()
    graph = px.bar(df_grouped, x='Categoria', y='Valor', title="Despesas Gerais")
    graph.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return graph
