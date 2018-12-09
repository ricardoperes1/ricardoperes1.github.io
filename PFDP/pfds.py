# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 16:05:11 2018

@author: ricar
"""

from flask import Flask, render_template, request,redirect,url_for
import mysql.connector
#from data import Eventos


conn = mysql.connector.connect(user='root',password='PFDS2018',host='localhost',database='myapp', auth_plugin='mysql_native_password')

app = Flask(__name__)
#Eventos = Eventos()
#EXEMPLO POST MySQL
# =============================================================================
# cur = conn.cursor()
# cur.execute("INSERT INTO users(password, username) VALUES(%s,%s)",("mellis","lucas",))
# conn.commit()
# cur.close()
# 
# =============================================================================

tasks = [{'id': 0,
        'titulo': 'Acabar o trabalho',
        'data': "acabar o trabalho para domingo",
        'feito': False},

        {'id': 0,
        'titulo': 'tirar carta',
        'data': 'ir no detran e fazer aula',
        'feito': True}]
    
        
    
@app.route("/login",methods=["GET","POST"])
def login():
    
  
    if request.method=="POST":
        senha = request.form['password']
        username = request.form['username']
        if username == "" or senha == "":
            return render_template("login.html")
        else:
            pass
        cur = conn.cursor(buffered=True)
        cur.execute("SELECT username,password FROM users WHERE username=%s",(username,))
        dados = cur.fetchone()
        cur.close()
        if dados == None:
            return render_template("login.html")
        else:
            if dados[0] == username and dados[1] == senha:
                return redirect(url_for("home"))
            else:
                return render_template("login.html")
        
    else:
        return render_template("login.html")
    return render_template('login.html')

   
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        name = request.form['nome']
        username = request.form['username']
        email = request.form['email']
        senha = request.form['password']
        if name == "" or username == "" or email == "" or senha == "":
            return render_template("register.html")
        else:
            pass
        cur = conn.cursor(buffered=True)
        cur.execute("INSERT INTO users(name,username,email,password) VALUES(%s,%s,%s,%s)",(name,username,email,senha))
        conn.commit()
        cur.close()
        cur.close()
        
        return redirect(url_for('login'))
         
    
    
    return render_template('register.html')




@app.route("/", methods=['POST', 'GET'])
def home():
    #mensagem_erro = ''
    if request.method == 'POST':
        if 'id' in request.form:
            id = int(request.form['id'])
            tasks[id]['feito'] = request.form['feito'] == 'True'
        else:
            titulo = request.form['titulo']
            data = request.form['data']
            
            novo_evento = {
                'id': len(tasks),
                'titulo': titulo,
                'data': data,
                'feito': False,
            }
            if len(titulo) > 0:
                tasks.append(novo_evento)
            else:
                return  render_template("home.html")
    return render_template('home.html',tasks=tasks)
# =============================================================================
# 
# =============================================================================
            
            
    
if __name__ == '__main__':
    app.run(debug=True)