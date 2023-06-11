from sqlalchemy import create_engine
import pandas as pd


def mysql_connection(host, user, passwd, database=None):
    engine = create_engine(
        f'mysql+pymysql://{user}:{passwd}@{host}/{database}'
    )
    return engine.connect()


conn = mysql_connection('localhost', 'pfelix', 'Secure987', 'MinhaCarteira')


_v_user = 'jsilva'


def categorias():
    query = 'SELECT IdCategoria, NomeCategoria, TipoCategoria FROM Categoria'
    df_list_cat = pd.read_sql(query, con=conn, index_col="IdCategoria")
    return df_list_cat


df_categorias = categorias()


def categorias_receita():
    df_cat = df_categorias
    df_categorias_receita = df_cat[
        df_cat.TipoCategoria != 'Debito'
        ].filter(items=['NomeCategoria'])
    return df_categorias_receita


df_categorias_receita = categorias_receita()
lista_categorias_receita = categorias_receita().values.tolist() 


def categorias_debito():
    df_cat = df_categorias
    df_categorias_debito = df_cat[
        df_cat.TipoCategoria != 'Receita'
        ].filter(items=['NomeCategoria'])
    return df_categorias_debito


df_categorias_debito = categorias_debito()
lista_categorias_debito = categorias_debito().values.tolist() 


def consulta_IdCategoria(_v_NomeCategoria):
    f_categoria = df_categorias.query(f'NomeCategoria == "{_v_NomeCategoria}"')
    l_categoria = f_categoria.index.to_list()
    categoria = int(l_categoria[0])
    return categoria

def recorrente():
    query = 'SELECT IdRecorrente, NomeRecorrente FROM Recorrente'
    df_recorrente = pd.read_sql(query, con=conn, index_col="IdRecorrente")
    return df_recorrente


df_recorrente = recorrente()
lista_recorrente = recorrente().filter(items=['NomeRecorrente']).values.tolist()


def consulta_IdRecorrente(_v_NomeRecorrente):
    f_recorrente = df_recorrente.query(f'NomeRecorrente == "{_v_NomeRecorrente}"')
    l_recorrente = f_recorrente.index.to_list()
    recorrente = l_recorrente[0]
    return recorrente



def bancos():
    query = "SELECT * FROM Banco"
    df_list_banco = pd.read_sql(query, con=conn, index_col="IdBanco")
    return df_list_banco


df_banco = bancos()


def contas(_v_user):
    query = f"""SELECT
                    IdConta,
                    IdUsuario,
                    NomeConta,
                    IdBanco,
                    CodAgencia,
                    CodConta,
                    Gerente,
                    TelGerente,
                    EmailGerente
                FROM Conta
                WHERE IdUsuario = '{_v_user}'
            """
    df_conta = pd.read_sql(query, con=conn, index_col='IdConta')
    return df_conta


df_conta = contas(_v_user)
lista_conta = contas(_v_user).filter(items=['NomeConta']).values.tolist()


def consulta_IdConta(_v_NomeConta):
    f_conta = df_conta.query(f'NomeConta == "{_v_NomeConta}"')
    l_conta = f_conta.index.to_list()
    conta = l_conta[0]
    return conta


def receita(_v_user):
    query = f"""SELECT
                    ID,
                    b.Data,
                    b.Valor,
                    e.NomeConta,
                    c.NomeCategoria,
                    d.NomeRecorrente,
                    CASE WHEN
                        b.Efetuado = 0
                            THEN 'Não Efetuado'
                            ELSE 'Efetuado' END
                        AS Efetuado,
                    b.Descricao
                FROM Receita b
                    INNER JOIN Categoria c ON b.IdCategoria = c.IdCategoria
                    INNER JOIN Recorrente d ON b.IdRecorrente = d.IdRecorrente
                    INNER JOIN Conta e ON b.IdConta = e.IdConta
                    WHERE b.Idusuario = '{_v_user}'
                """
    df_receita = pd.read_sql(query, con=conn, index_col='ID')
    return df_receita


df_receita = receita(_v_user)


def debito(_v_user):
    query = f"""SELECT
                    ID,
                    b.Data,
                    (b.Valor)*-1,
                    e.NomeConta,
                    c.NomeCategoria,
                    d.NomeRecorrente,
                    CASE WHEN
                        b.Efetuado = 0
                            THEN 'Não Efetuado'
                            ELSE 'Efetuado' END
                        AS Efetuado,
                    b.Descricao
                FROM Debito b
                    INNER JOIN Categoria c ON b.IdCategoria = c.IdCategoria
                    INNER JOIN Recorrente d ON b.IdRecorrente = d.IdRecorrente
                    INNER JOIN Conta e ON b.IdConta = e.IdConta
                    WHERE b.Idusuario = '{_v_user}'
                """
    df_receita = pd.read_sql(query, con=conn, index_col='ID')
    return df_receita


df_debito = debito(_v_user)

def efetuado():
    data_structure = {
        'IdEfetuado': [0, 1],
        'NomeEfetuado': ['Não Efetuado', 'Efetuado'],
    }
    df_efetuado = pd.DataFrame(data_structure)
    return df_efetuado


df_efetuado = efetuado()
lista_efetuado = efetuado().filter(items=['NomeEfetuado']).values.tolist()

df = df_receita.tail(1)

# def cadastrar_receita(user, conta, data, valor, categoria, recorrente, efetuado, descricao):
#     _v_user = user
#     _v_conta = conta
#     _v_data = data
#     _v_valor = valor
#     _v_categoria = categoria
#     _v_recorrente = recorrente
#     _v_efetuado = efetuado
#     _v_descricao = descricao

