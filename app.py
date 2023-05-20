#!.venv/bin/python3

import os
from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'pfelix'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Secure987'
app.config['MYSQL_DATABASE_DB'] = 'MinhaCarteira'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/listabancos',methods=['POST','GET'])
def listaBancos():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute ('select IdBanco, NomeBanco from Banco')
        data = cursor.fetchall()
        print(data[0]);

        conn.commit()
        return render_template('listabancos.html', datas=data)

    except Exception as error:
        return json.dumps({'error':str(error)})
    finally:
        cursor.close()
        conn.close()

@app.route('/cadastrobanco')
def cadastroBanco():
    return render_template('cadastrobanco.html')

@app.route('/cadbanco',methods=['POST','GET'])
def cadastro_Banco():
    try:
        codBanco = int(request.form['codBanco'])
        nomeBanco = request.form['nomeBanco']
        if codBanco and nomeBanco:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_criaBanco',(codBanco, nomeBanco))
            data = cursor.fetchall()
            if len(data) == 0:
                conn.commit()           
            else:
                return json.dumps({'error':str(data[0])})
            return render_template('index.html')
    except Exception as error:
        return json.dumps({'error':str(error)})
    finally:
        cursor.close() 
        conn.close()

@app.route('/listacategoria',methods=['POST','GET'])
def listaCategoria():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute ('select IdCategoria, NomeCategoria, TipoCategoria from Categoria')
        data = cursor.fetchall()
        print(data[0]);
        conn.commit()
        return render_template('listacategoria.html', datas=data)

    except Exception as error:
        return json.dumps({'error':str(error)})
    finally:
        cursor.close()
        conn.close()

@app.route('/cadastrocategoria')
def cadastroCategoria():
    return render_template('cadastrocategoria.html')

@app.route('/cadcategoria',methods=['POST','GET'])
def cadastro_Categoria():
    try:
        _nomeCategoria = request.form['NomeCategoria']
        _tipoCategoria = request.form['tipoCategoria']
        if _nomeCategoria and _tipoCategoria:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_CriaCategoria',(_nomeCategoria, _tipoCategoria))
            data = cursor.fetchall()
            if len(data) == 0:
                conn.commit()           
            else:
                return json.dumps({'error':str(data[0])})
            return render_template('index.html')
    except Exception as error:
        return json.dumps({'error':str(error)})
    
    finally:
        cursor.close() 
        conn.close()

@app.route('/listareceita',methods=['POST','GET'])
def listaReceita():
    try:
        _v_usuario = 'jsilva'
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute (f"""
            SELECT 
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
                WHERE b.Idusuario = '{_v_usuario}'
            """)
        data = cursor.fetchall()
        conn.commit()
        return render_template('listareceita.html', datas=data)

    except Exception as error:
        return json.dumps({'error':str(error)})
    finally:
        cursor.close()
        conn.close()

@app.route('/cadastroreceita')
def cadastroReceitas():
    return render_template('cadastroreceita.html')

@app.route('/cadreceita',methods=['POST','GET'])
def cadastro_Receita():
    try:
        _v_id_user = 'jsilva'
        _v_id_conta = '34112340123456'
        _v_dt = request.form['Data']
        _v_vl = float(request.form['Valor'])
        _v_idcat = int(request.form['IdCategoria'])
        _v_idrec = int(request.form['IdRecorrente'])
        _v_efet = int(request.form['Efetuado'])
        _v_desc = request.form['Descricao']
        if _v_dt and _v_vl and _v_idcat and _v_idrec and _v_efet and _v_desc and _v_id_conta:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_Receita',(_v_id_user, _v_dt, _v_vl, _v_id_conta, _v_idcat, _v_idrec, _v_efet, _v_desc))
            data = cursor.fetchall()
            if len(data) == 0:
                conn.commit()
            else:
                return json.dumps({'error':str(data[0])})
            return render_template('index.html')
    except Exception as error:
        return json.dumps({'error':str(error)})
    finally:
        cursor.close() 
        conn.close()

@app.route('/listadebito',methods=['POST','GET'])
def listaDebito():
    try:
        _v_usuario = 'jsilva'
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute (f"""
            SELECT 
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
                WHERE b.IdUsuario = '{_v_usuario}';""")
        data = cursor.fetchall()
        conn.commit()
        return render_template('listadebito.html', datas=data)

    except Exception as error:
        return json.dumps({'error':str(error)})
    finally:
        cursor.close()
        conn.close()

@app.route('/cadastrodebito')
def cadastroDebito():
    return render_template('cadastrodebito.html')

@app.route('/caddebito',methods=['POST','GET'])
def cadastro_Debito():
    try:
        _v_id_user = 'jsilva'
        _v_id_conta = '34112340123456'
        _v_dt = request.form['Data']
        _v_vl = float(request.form['Valor'])
        _v_idcat = int(request.form['IdCategoria'])
        _v_idrec = int(request.form['IdRecorrente'])
        _v_efet = int(request.form['Efetuado'])
        _v_desc = request.form['Descricao']
        if _v_dt and _v_vl and _v_idcat and _v_idrec and _v_efet and _v_desc and _v_id_conta:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_Debito',(_v_id_user, _v_dt, _v_vl, _v_id_conta, _v_idcat, _v_idrec, _v_efet, _v_desc))
            data = cursor.fetchall()
            if len(data) == 0:
                conn.commit()
            else:
                return json.dumps({'error':str(data[0])})
            return render_template('index.html')
    except Exception as error:
        return json.dumps({'error':str(error)})
    finally:
        cursor.close() 
        conn.close()

@app.route('/extrato',methods=['POST','GET'])
def extrato():
    try:
        _v_usuario = 'jsilva'
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(f"""
            (
                SELECT 
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
                    WHERE b.Idusuario = '{_v_usuario}')
            UNION ALL
            (
                SELECT 
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
                WHERE b.IdUsuario = '{_v_usuario}');
        """)
        data = cursor.fetchall()
        conn.commit()
    
        return render_template('extrato.html', datas=data)

    except Exception as error:
        return json.dumps({'error':str(error)})
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8081))
    app.run(host='0.0.0.0', port=port)