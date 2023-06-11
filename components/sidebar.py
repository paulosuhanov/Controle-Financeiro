from datetime import datetime, date
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app
from db_backend import list_conta, list_cat_receita, list_cat_despesa
import pandas as pd

_v_user = 'paulo.felix'

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto"
}

# ========= Layout ========= #
layout = dbc.Col([
    dbc.Row([
        # ===== Titulo App
        dbc.Card(
            [
                html.H2(
                    "Minha Carteira",
                    className="text-primary",
                    style={
                        "text-align": "center"
                    }
                ),
                html.P("Por Paulo Felix", className="text-info"),
                html.Hr(),
            ]    
        )
    ]),
    # Card Saldo Despesas
    dbc.Row([
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Despesas'),
                    html.H5(
                        '- R$ 5400,00',
                        id='saldo-despesas',
                        style={}
                    )], style={
                        'padding-left': '20px',
                        'padding-top': '5px'
                    }),
                dbc.Card(
                    html.Div(
                        className='fa fa-meh-o',
                        style=card_icon
                    ),
                    color='danger',
                    style={
                        'maxWidth': 70,
                        'height': 90,
                        'margin-left': '-10px'
                    }
                ),
                html.Br()
            ])
        ])
    ], style={
        'margin-top': '5px',
        'padding-left': '-10px',
        'padding-right': '-10px',
        }),
    # Card Saldo Receita
    dbc.Row([
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Receita'),
                    html.H5(
                        'R$ 5400,00',
                        id='saldo-receitas',
                        style={}
                    )], style={
                        'padding-left': '20px',
                        'padding-top': '5px'
                    }),
                dbc.Card(
                    html.Div(
                        className='fa fa-smile-o',
                        style=card_icon
                    ),
                    color='success',
                    style={
                        'maxWidth': 70,
                        'height': 90,
                        'margin-left': '-10px'
                    }
                ),
                html.Hr()
            ])
        ])
    ], style={
        'margin-top': '5px',
        'padding-left': '-10px',
        'padding-right': '-10px',
        }),
    # Card Saldo Total
    dbc.Row([
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Saldo Total'),
                    html.H5(
                        'R$ 5400,00',
                        id='saldo-total',
                        style={}
                    )
                ], style={
                    'padding-left': '20px',
                    'padding-top': '5px',
                    }
                ),
                dbc.Card(
                    html.Div(
                        className='fa fa-university',
                        style=card_icon
                    ),
                    color='warning',
                    style={
                        'maxWidth': 70,
                        'height': 90,
                        'margin-left': '-10px'
                    }
                ),
                html.Hr(),
            ])
        ]),
    ], style={
        'margin-top': '5px',
        'padding-left': '-10px',
        'padding-right': '-10px',
        'margin-bottom': '20px'
        }),
    # ====== Sessão Nova Receita e Despesas
    dbc.Row([
        dbc.Col([
            dbc.Button(
                id='open-nova-receita',
                color='success',
                children=['+ Receita']
            )
        ], md=6),
        dbc.Col([
            dbc.Button(
                id='open-nova-despesa',
                color='warning',
                children=['- Despensa']
            )
        ], md=6),
    ]),
    # Modal Receita
    dbc.Modal([
        dbc.ModalHeader(
            dbc.ModalTitle('Adicionar Receita')
            ), dbc.ModalBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Conta: "),
                        dbc.Select(
                            id="select-conta-receita",
                            options=[
                                {
                                    'label': i, 'value': i
                                } 
                                for i in list_conta
                            ],
                            value=list_conta[0],
                            style={
                                'width': '90%',
                                'margin-left': '5px',
                                'margin-right': '5px'}
                        )
                    ], width=4),
                    dbc.Col([
                        dbc.Label("Data: "),
                        dcc.DatePickerSingle(
                            id="data-receita",
                            min_date_allowed=date(2020, 1, 1),
                            max_date_allowed=date(2030, 12, 31),
                            date=datetime.today(),
                            display_format='DD / MM / YYYY',
                            style={
                                'width': '90%',
                                'margin-left': '5px',
                                'margin-right': '5px'}
                        ),
                    ], width=4),
                    dbc.Col([
                        dbc.Label("Valor: "),
                        dbc.Input(
                            id="valor-receita",
                            placeholder='R$ 100.00',
                            value="",
                            style={
                                'width': '90%',
                                'margin-left': '5px',
                                'margin-right': '5px'})
                    ], width=4)
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Categoria: "),
                        dbc.Select(
                            id="select-categoria-receita",
                            options=[
                                {
                                    'label': i, 'value': i
                                } 
                                for i in list_cat_receita
                            ],
                            value=list_cat_receita[0],
                            style={
                                'width': '90%',
                                'margin-left': '5px',
                                'margin-right': '5px'}
                        )
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Opções Extras"),
                        dbc.Checklist(
                            options=[
                                {
                                    "label": "Foi Creditado",
                                    "value": 1,
                                },
                                {
                                    "label": "Receita Recorrente",
                                    "value": 2
                                }
                            ],
                            value=[1],
                            id="switches-receita",
                            switch=True
                        ),
                    ], width=6),
                ], style={'margin-top': '25px'}
                ),
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Descrição: '),
                        dbc.Input(
                            id="descricao-receita",
                            placeholder="Ex.: dividendos, herança...",
                            style={
                                'width': '90%',
                                'margin-left': '5px',
                                'margin-right': '5px'}
                        ),
                    ], width=12),
                ], style={'margin-top': '25px'}
                ),
                dbc.Row([
                    html.Br(),
                ]),
                dbc.Row([
                    dbc.Accordion([
                        dbc.AccordionItem(
                            children=[
                                dbc.Row([
                                    dbc.Col([
                                        html.Legend(
                                            "Adicionar Categoria",
                                            style={'color': 'green'}
                                        ),
                                        dbc.Input(
                                            type="text",
                                            placeholder="Nova Categoria...",
                                            id="input-add-cat-receita",
                                            value=""
                                        ),
                                        html.Br(),
                                        dbc.Button(
                                            'Adicionar',
                                            id="btn-add-cat-receita",
                                            className="btn btn-success",
                                            style={"margin-top": "20px"}
                                        ),
                                        html.Br(),
                                        html.Div(
                                            id="div-add-categoria-receita",
                                            style={}
                                        )
                                    ], width=5),
                                    dbc.Col([
                                    ], width=2),
                                    dbc.Col([
                                        html.Legend(
                                            'Excluir Categoria',
                                            style={'color': 'red'}
                                        ),
                                        dbc.Checklist(
                                            id='checklist-select-cat-receita',
                                            options=[
                                                {
                                                'label': i, 'value': i
                                                } 
                                                for i in list_cat_receita
                                            ],
                                            value=[],
                                            label_checked_style={
                                                'color': 'red'
                                            },
                                            input_checked_style={
                                                'backgroundColor': 'blue',
                                                'boderColor': 'orange'
                                            },
                                        ),
                                        dbc.Button(
                                            'Remover',
                                            id='btn-remove-cat-receita',
                                            className="btn btn-remove",
                                            color='warning',
                                            style={'margin-top': '20px'}
                                        )
                                    ], width=5),
                                ]),
                            ], title='Adicionar / Remover Categorias'
                        )
                    ],  
                    flush=True,
                    start_collapsed=True,
                    id='accordion-receita'),
                    html.Div(
                        id='cat-receita',
                        style={'padding-top': '20px'}
                    ),
                    dbc.ModalFooter([
                        dbc.Button(
                            "Adicionar Receita",
                            id="salvar-receita",
                            color="warning"
                        ),
                        dbc.Popover(
                            dbc.PopoverBody(
                                "Receita Salva"
                            ),
                            target="salvar-receita",
                            placement="left",
                            trigger="click"
                        ),
                    ]),
                ], 
                style={
                    'margin-top': '25px'
                }
                ),
            ]),
        ],
            id='modal-nova-receita',
            size='lg',
            is_open=False,
            centered=True,
            backdrop=True,
            style={
                    'background': "rgb(17, 140, 79, 0.05)"
            }
    ),

    # Modal Despesa
    dbc.Modal([
        dbc.ModalHeader(
            dbc.ModalTitle('Adicionar Despesa')
            ),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Conta: "),
                        dbc.Select(
                            id="select-conta-despesa",
                            options=[
                                {
                                    'label': i, 'value': i
                                } 
                                for i in list_conta
                            ],
                            value=list_conta[0],
                            style={
                                'width': '90%',
                                'margin-left': '5px',
                                'margin-right': '5px'}
                        )
                    ], width=4),
                    dbc.Col([
                        dbc.Label("Data: "),
                        dcc.DatePickerSingle(
                            id="data-despesa",
                            min_date_allowed=date(2020, 1, 1),
                            max_date_allowed=date(2030, 12, 31),
                            date=datetime.today(),
                            display_format='DD / MM / YYYY',
                            style={
                                'width': '90%',
                                'margin-left': '5px',
                                'margin-right': '5px'}
                        ),
                    ], width=4),
                    dbc.Col([
                        dbc.Label("Valor: "),
                        dbc.Input(
                            id="valor-despesa",
                            placeholder='R$ 100.00',
                            value="",
                            style={
                                'width': '90%',
                                'margin-left': '5px',
                                'margin-right': '5px'})
                    ], width=4)
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Categoria: "),
                        dbc.Select(
                            id="select-categoria-despesa",
                            options=[
                                {
                                    'label': i, 'value': i
                                } 
                                for i in list_cat_despesa
                            ],
                            value=list_cat_despesa[0],
                            style={
                                'width': '90%',
                                'margin-left': '5px',
                                'margin-right': '5px'}
                        )
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Opções Extras"),
                        dbc.Checklist(
                            options=[
                                {
                                    "label": "Foi Debitado",
                                    "value": 1,
                                },
                                {
                                    "label": "Despesa Recorrente",
                                    "value": 2
                                }
                            ],
                            value=[1],
                            id="switches-despesa",
                            switch=True
                        ),
                    ], width=6),
                ], style={'margin-top': '25px'}
                ),
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Descrição: '),
                        dbc.Input(
                            id="descricao-despesa",
                            placeholder="Ex.: dividendos, herança...",
                            style={
                                'width': '90%',
                                'margin-left': '5px',
                                'margin-right': '5px'}
                        ),
                    ], width=12),
                ], style={'margin-top': '25px'}
                ),
                dbc.Row([
                    html.Br(),
                ]),
                dbc.Row([
                    dbc.Accordion([
                        dbc.AccordionItem(
                            children=[
                                dbc.Row([
                                    dbc.Col([
                                        html.Legend(
                                            "Adicionar Categoria",
                                            style={'color': 'green'}
                                        ),
                                        dbc.Input(
                                            type="text",
                                            placeholder="Nova Categoria...",
                                            id="input-add-cat-despesa",
                                            value=""
                                        ),
                                        html.Br(),
                                        dbc.Button(
                                            'Adicionar',
                                            id="btn-add-cat-despesa",
                                            className="btn btn-success",
                                            style={"margin-top": "20px"}
                                        ),
                                        html.Br(),
                                        html.Div(
                                            id="div-add-categoria-despesa",
                                            style={}
                                        )
                                    ], width=5),
                                    dbc.Col([
                                    ], width=2),
                                    dbc.Col([
                                        html.Legend(
                                            'Excluir Categoria',
                                            style={'color': 'red'}
                                        ),
                                        dbc.Checklist(
                                            id='checklist-select-cat-despesa',
                                            options=[
                                                {
                                                    'label': i, 'value': i
                                                } 
                                                for i in list_cat_despesa
                                            ],
                                            value=[],
                                            label_checked_style={
                                                'color': 'red'
                                            },
                                            input_checked_style={
                                                'backgroundColor': 'blue',
                                                'boderColor': 'orange'
                                            },
                                        ),
                                        dbc.Button(
                                            'Remover',
                                            id='btn-remove-cat-despesa',
                                            className="btn btn-remove",
                                            color='warning',
                                            style={'margin-top': '20px'}
                                        )
                                    ], width=5),
                                ]),
                            ], title='Adicionar / Remover Categorias'
                        )
                    ],  
                    flush=True,
                    start_collapsed=True,
                    id='accordion-despesa'),
                    html.Div(
                        id='cat-despesa',
                        style={'padding-top': '20px'}
                    ),
                    dbc.ModalFooter([
                        dbc.Button(
                            "Adicionar Despesa",
                            id="salvar-despesa",
                            color="warning"
                        ),
                        dbc.Popover(
                            dbc.PopoverBody(
                                "Despesa Salva"
                            ),
                            target="salvar-despesa",
                            placement="left",
                            trigger="click"
                        ),
                    ]),
                ], 
                style={
                    'margin-top': '25px'
                }
                ),
            ]),
        ],
            id='modal-nova-despesa',
            size='lg',
            is_open=False,
            centered=True,
            backdrop=True,
            style={
                    'background': "rgb(17, 140, 79, 0.05)"
            }
    ),
    html.Hr(),
    # ====== Sessão Navegação
    dbc.Nav([
        dbc.NavLink(
            "Dashboard",
            href="/dashboards",
            active="exact"
        ),
        dbc.NavLink(
            "Extrato de Receitas",
            href="/receitas",
            active="exact"),
        dbc.NavLink(
            "Extrato de Despesas",
            href="/despesas",
            active="exact"),
    ],
    vertical=True,
    pills=True,
    id="nav_buttons",
    style={"margin-botton": "50px"}
    ),
], id='sidebar_completa')

# =========  Callbacks  =========== #

# === Despesa === Popup
@app.callback(
    Output('modal-nova-despesa', 'is_open'),
    Input('open-nova-despesa', 'n_clicks'),
    State('modal-nova-despesa', 'is_open')
)
def modal_despesa(n1, is_open):
    if n1:
        return not is_open

# ===Despesa === Adcionar e Remover Categorias
@app.callback(
    [
        Output('select-categoria-despesa', 'options'),
        Output('checklist-select-cat-despesa', 'options'),
        Output('checklist-select-cat-despesa', 'value'),
        Output('store-cat-despesas', 'data')
    ],
    [
        Input('btn-add-cat-despesa', 'n_clicks'),
        Input('btn-remove-cat-despesa', 'n_clicks')
    ],
    [
        State('input-add-cat-despesa', 'value'),
        State('checklist-select-cat-despesa', 'value'),
        State('store-cat-despesas', 'data')
    ]
)
def add_rem_cat_despesa(n_c1, n_c2, add_cat, check_rem_cat, dict_cat):
    new_cat = list(dict_cat['Categoria'].values())

    if n_c1 and not (add_cat == '' or add_cat == None):
        new_cat = new_cat + [add_cat] if add_cat not in new_cat else new_cat

    if n_c2:
        if len(check_rem_cat) > 0:
            new_cat = [i for i in new_cat if i not in check_rem_cat]  
    
    opt_despesa = [{'label': i, 'value': i} for i in new_cat]
    df_cat_despesas = pd.DataFrame(new_cat, columns=['Categoria'])
    df_cat_despesas.to_csv('df_cat_despesa.csv')
    data_return = df_cat_despesas.to_dict()
    return [opt_despesa, opt_despesa, [], data_return]

# === Despesa === Adicionar Formulário
@app.callback(
    Output('store-despesas', 'data'),

    Input('salvar-despesa', 'n_clicks'),
    [
        State('select-conta-despesa', 'value'),
        State('data-despesa', 'date'),
        State('valor-despesa', 'value'),
        State('select-categoria-despesa', 'value'),
        State('switches-despesa', 'value'),
        State('descricao-despesa', 'value'),
        State('store-despesas', 'data')
    ]
)
def save_form_despesa(n, conta, data, valor, categoria, switches, descricao, dict_despesas):
    df_despesas = pd.DataFrame(dict_despesas)
    if n and not (valor == "" or valor == None):
        _v_data = pd.to_datetime(data).date()
        _v_valor = round(float(valor.replace(',', '.')), 2)
        _v_categoria = categoria[0] if type(categoria) == list else categoria
        _v_conta = conta[0] if type(conta) == list else conta
        _v_efetuado = 1 if 1 in switches else 0
        _v_recorrente = 1 if 2 in switches else 0
        _v_descricao = descricao

        df_despesas.loc[df_despesas.shape[0]] = [_v_user, _v_data, _v_valor, _v_conta, _v_categoria, _v_recorrente, _v_efetuado, _v_descricao]
        df_despesas.to_csv('df_despesas.csv')
    data_return = df_despesas.to_dict()
    return data_return

# === Receita === Popup
@app.callback(
    Output('modal-nova-receita', 'is_open'),
    Input('open-nova-receita', 'n_clicks'),
    State('modal-nova-receita', 'is_open')
)
def modal_receita(n1, is_open):
    if n1:
        return not is_open

# === Receita === Adcionar e Remover Categorias
@app.callback(
    [
        Output('select-categoria-receita', 'options'),
        Output('checklist-select-cat-receita', 'options'),
        Output('checklist-select-cat-receita', 'value'),
        Output('store-cat-receitas', 'data')
    ],
    [
        Input('btn-add-cat-receita', 'n_clicks'),
        Input('btn-remove-cat-receita', 'n_clicks')
    ],
    [
        State('input-add-cat-receita', 'value'),
        State('checklist-select-cat-receita', 'value'),
        State('store-cat-receitas', 'data')
    ]
)
def add_rem_cat_receitas(n_c1, n_c2, add_cat, check_rem_cat, dict_cat):
    new_cat = list(dict_cat['Categoria'].values())

    if n_c1 and not (add_cat == '' or add_cat == None):
        new_cat = new_cat + [add_cat] if add_cat not in new_cat else new_cat

    if n_c2:
        if len(check_rem_cat) > 0:
            new_cat = [i for i in new_cat if i not in check_rem_cat]  
    
    opt_receita = [{'label': i, 'value': i} for i in new_cat]
    df_cat_receitas = pd.DataFrame(new_cat, columns=['Categoria'])
    df_cat_receitas.to_csv('df_cat_receita.csv')
    data_return = df_cat_receitas.to_dict()
    return [opt_receita, opt_receita, [], data_return]

# === Receita === Adicionar Formulário
@app.callback(
    Output('store-receitas', 'data'),

    Input('salvar-receita', 'n_clicks'),
    [
        State('select-conta-receita', 'value'),
        State('data-receita', 'date'),
        State('valor-receita', 'value'),
        State('select-categoria-receita', 'value'),
        State('switches-receita', 'value'),
        State('descricao-receita', 'value'),
        State('store-receitas', 'data')
    ]
)
def save_form_receita(n, conta, data, valor, categoria, switches, descricao, dict_receitas):

    df_receitas = pd.DataFrame(dict_receitas)

    if n and not (valor == "" or valor == None):
        _v_data = pd.to_datetime(data).date()
        _v_valor = round(float(valor.replace(',', '.')), 2)
        _v_categoria = categoria[0] if type(categoria) == list else categoria
        _v_conta = conta[0] if type(conta) == list else conta
        _v_efetuado = 1 if 1 in switches else 0
        _v_recorrente = 1 if 2 in switches else 0
        _v_descricao = descricao

        df_receitas.loc[df_receitas.shape[0]] = [_v_user, _v_data, _v_valor, _v_conta, _v_categoria, _v_recorrente, _v_efetuado, _v_descricao]
        df_receitas.to_csv('df_receitas.csv')

    data_return = df_receitas.to_dict()
    return data_return
