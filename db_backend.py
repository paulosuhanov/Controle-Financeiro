import pandas as pd
import os

if ("df_despesas.csv" in os.listdir()) and ("df_receitas.csv" in os.listdir()):
    df_despesas = pd.read_csv("df_despesas.csv", index_col=0, parse_dates=['Data'], dayfirst=False)
    df_receitas = pd.read_csv("df_receitas.csv", index_col=0, parse_dates=['Data'], dayfirst=False)
    df_despesas["Data"] = pd.to_datetime(df_despesas["Data"])
    df_receitas["Data"] = pd.to_datetime(df_receitas["Data"])
    df_despesas["Data"] = df_despesas["Data"].apply(lambda x: x.date())
    df_receitas["Data"] = df_receitas["Data"].apply(lambda x: x.date())

else:
    data_structure = {
        'Usuario': [],
        'Data': [],
        'Valor': [],
        'Conta': [],
        'Categoria': [],
        'Recorrente': [],
        'Efetuado': [],
        'Descrição': []
        }

    df_receitas = pd.DataFrame(data_structure)
    df_despesas = pd.DataFrame(data_structure)
    df_despesas.to_csv("df_despesas.csv")
    df_receitas.to_csv("df_receitas.csv")


if ("df_cat_receita.csv" in os.listdir()) and ("df_cat_despesa.csv" in os.listdir()) and ("df_conta.csv" in os.listdir()):
    df_cat_receita = pd.read_csv("df_cat_receita.csv", index_col=0)
    df_cat_despesa = pd.read_csv("df_cat_despesa.csv", index_col=0)
    df_conta = pd.read_csv("df_conta.csv", index_col=0)
    list_cat_receita = df_cat_receita.values.tolist()
    list_cat_despesa = df_cat_despesa.values.tolist()
    list_conta = df_conta.values.tolist()


else:
    cat_receita = {
        'Categoria': [
            "Salário",
            "Investimentos",
            "Comissão"
        ]
    }
    cat_despesa = {
        'Categoria': [
            "Alimentação",
            "Aluguel",
            "Gasolina",
            "Saúde",
            "Lazer"
        ]
    }
    cat_conta = {
        'Conta': [
            "Itau Familia",
            "Itau Pessoal",
            "Nubank Pessoal",
            "BTG Investimento"
        ]
    }
    df_cat_receita = pd.DataFrame(cat_receita, columns=['Categoria'])
    df_cat_despesa = pd.DataFrame(cat_despesa, columns=['Categoria'])
    df_conta = pd.DataFrame(cat_conta, columns=['Conta'])
    df_cat_receita.to_csv("df_cat_receita.csv")
    df_cat_despesa.to_csv("df_cat_despesa.csv")
    df_conta.to_csv("df_conta.csv")
