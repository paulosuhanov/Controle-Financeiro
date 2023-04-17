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
            cursor.callproc('sp_criaBancoCustomizado',(codBanco, nomeBanco))
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

@app.route('/listacatreceita',methods=['POST','GET'])
def listaCatReceita():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute ('select ID, CategoriaReceita from CatReceita')
        data = cursor.fetchall()
        print(data[0]);
        conn.commit()
        return render_template('listacatreceita.html', datas=data)

    except Exception as error:
        return json.dumps({'error':str(error)})
    finally:
        cursor.close()
        conn.close()

@app.route('/cadastrocatreceita')
def cadastroCatReceitas():
    return render_template('cadastrocatreceita.html')

@app.route('/cadcatreceita',methods=['POST','GET'])
def cadastro_CatReceita():
    try:
        _nomeCatReceita = request.form['nomeCatReceita']
        if _nomeCatReceita:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('insert into CatReceita (CategoriaReceita) VALUES (%s)', (_nomeCatReceita))
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
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute ('select DtEntrada, VlReceita, IdCatReceita, DescReceita from Receita')
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
        v_DtEntrada = request.form['DtEntrada']
        v_VlReceita = float(request.form['VlReceita'])
        v_IdCatReceita = int(request.form['IdCatReceita'])
        v_DescReceita = request.form['DescReceita']
        if v_DtEntrada and v_VlReceita and v_IdCatReceita and v_DescReceita:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('insert into Receita (DtEntrada, VlReceita, IdCatReceita, DescReceita) VALUES (%s, %s, %s, %s)',(v_DtEntrada, v_VlReceita, v_IdCatReceita, v_DescReceita))
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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)