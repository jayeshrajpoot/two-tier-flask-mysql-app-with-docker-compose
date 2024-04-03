import os
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from urllib.parse import quote

app = Flask(__name__)

#Configure MYSQL from environment variables
app.config['MYSQL_HOST']=os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER']=os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD']=os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB']=os.environ.get('MYSQL_DB')

#Initialize MYSQL
mysql = MySQL(app)

@app.route('/')
def hello():
    cur = mysql.connection.cursor()
    cur.execute('SELECT message FROM messages')
    messages = cur.fetchall()
    cur.close()
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    new_message = request.form.get('new_message')
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('hello'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

