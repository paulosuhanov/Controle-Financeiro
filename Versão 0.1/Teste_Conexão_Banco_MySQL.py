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

v_item = 'Emprestimo4'
conn = mysql.connect()
cursor = conn.cursor()
cursor.execute('insert into CatReceita (CategoriaReceita) VALUES (%s)', (v_item))
#cursor.callproc('sp_CriaCategoriaReceita',(v_item))
data = cursor.fetchall()
print(data);

conn.commit()
cursor.close()
conn.close()
