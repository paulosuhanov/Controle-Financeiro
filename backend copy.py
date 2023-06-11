from sqlalchemy import create_engine
import pandas as pd


def mysql_connection(host, user, passwd, database=None):
    engine = create_engine(
        f'mysql+pymysql://{user}:{passwd}@{host}/{database}'
    )
    return engine.connect()


conn = mysql_connection('localhost', 'pfelix', 'Secure987', 'MinhaCarteira')


_v_user = 'jsilva'

# Listar bancos cadastrados


def lista_banco():
    query = "SELECT * FROM Banco"
    df_list_bank = pd.read_sql(query, con=conn, index_col="IdBanco")
    return df_list_bank


def cadastro_banco(_v_cod_banco, _v_nome_banco):
    query = "SELECT * FROM Banco"
    df_list_bank = pd.read_sql(query, con=conn, index_col="IdBanco")

# Consultar Banco


def consulta_banco(_v_num_bank):
    num_bank = _v_num_bank
    query = f"SELECT * FROM Banco WHERE IdBanco = {num_bank}"
    df_consult_bank = pd.read_sql(query, con=conn, index_col="IdBanco")
    return df_consult_bank

# Listar Categorias Cadastradas


def lista_categoria():
    query = "SELECT IdCategoria, NomeCategoria, TipoCategoria FROM Categoria"
    df_list_cat = pd.read_sql(query, con=conn, index_col="IdCategoria")
    return df_list_cat

def cadastra_categoria():
    pass

def consulta_categoria(_v_categoria):
    pass

## Listar Debitos
def lista_receita():
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

def cadastra_receita():
    pass

def consulta_receita():
    pass

#List Debito
def lista_debito():
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

def cadastra_receita():
    pass

def consulta_receita():
    pass

