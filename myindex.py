from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from app import app
from components import sidebar, dashboards, extrato, receitas, despesas
from db_backend import df_receitas, df_despesas, df_cat_receita, df_cat_despesa, df_conta

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto"
}

# =========  Layout  =========== #

content = html.Div(id="page-content")

app.layout = dbc.Container(children=[
    dcc.Store(id='store-receitas', data=df_receitas.to_dict()),
    dcc.Store(id='store-despesas', data=df_despesas.to_dict()),
    dcc.Store(id='store-cat-receitas', data=df_cat_receita.to_dict()),
    dcc.Store(id='store-cat-despesas', data=df_cat_despesa.to_dict()),
    dcc.Store(id='store-conta', data=df_conta.to_dict()),
    dbc.Row([
        # Coluna com o Sidebar
        dbc.Col([
            dcc.Location(id='url'),
            sidebar.layout
        ], md=2),
        # Coluna com o Dashboard e Extrato
        dbc.Col([
            html.Div(id="page-content")
        ], md=10)
    ])
], fluid=True)

###### Callbacks


@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def render_page(pathname):
    if pathname == '/' or pathname == '/dashboards':
        return dashboards.layout
    elif pathname == '/receitas':
        return receitas.layout
    elif pathname == '/despesas':
        return despesas.layout

@app.callback(
    [
    Output('saldo-receitas', 'children'),
    Output('saldo-despesas', 'children'),
    Output('saldo-total', 'children')
    ],
    [
    Input('store-receitas', 'data'),
    Input('store-despesas', 'data')
    ]
)
def soma_valores(dict_receitas, dict_despesas):
    df_receita = pd.DataFrame(dict_receitas)
    df_despesa = pd.DataFrame(dict_despesas)
    soma_receitas = float(df_receita['Valor'].sum())
    soma_despesas = float(df_despesa['Valor'].sum())
    soma_total = soma_receitas - soma_despesas
    return ([f"R$ {soma_receitas:.2f}", f"R$ {soma_despesas:.2f}", f"R$ {soma_total:.2f}"])


if __name__ == '__main__':
    app.run_server(port=8051, debug=False)
