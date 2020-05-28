from flask import Flask, render_template, request, redirect, url_for, session, flash
import configparser
import re
import pymysql
#from mysql_query import *

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)

app.secret_key = 'loggedin'

def db_connection():
    db = pymysql.connect(host=config['mysql_db']['host'],
         user = config['mysql_db']['user'],
         password = config['mysql_db']['password'],
         database = config['mysql_db']['database'],
         autocommit = config['mysql_db']['autocommit'])
    #cursor = db.cursor()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return cursor

def connection():
    conn = pymysql.connect(host=config['mysql_db']['host'],
           user = config['mysql_db']['user'],
           password = config['mysql_db']['password'],
           database = config['mysql_db']['database'],
           autocommit = config['mysql_db']['autocommit'])
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        print("inside login >>>>>>>>>>>>")
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = db_connection()
        select_query = 'SELECT * FROM user_credentials WHERE username = %s AND password = MD5(%s)', (username, password)
        cursor.execute(select_query)
        # Fetch one record and return result
        user_credentials = cursor.fetchone()
        # If account exists in accounts table in out database
        if user_credentials:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['username'] = user_credentials['username']
            # Redirect to home page
            return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            #msg = 'Incorrect username/password!'
            return 'Incorrect username/password!'
    return render_template('login.html', msg='')


#@app.route('/register', methods=['GET', 'POST'])
@app.route('/register', methods=['POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        print("inside register >>>>>>>>>>>>>>>")
        # Create variables for easy access
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']
        #conf_password = request.form['conf_password']
        email = request.form['email']
        cursor = db_connection()
        # Check if account exists using MySQL
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_credentials WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            print("inside else condition >>>>>>>>>>>>>>.")
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO user_credentials VALUES (%s, %s, %s, MD5(%s), %s)',
                          (username, firstname, lastname, password, email))
            conn = connection()
            conn.commit()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('login.html', msg=msg)
    #return render_template('mohit.html', msg=msg)

@app.route('/administration', methods=['POST', 'GET'])
def administration():
    return "Administration section"

if __name__ == '__main__':
    app.run()
