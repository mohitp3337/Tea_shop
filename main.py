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
                        database = config['mysql_db']['database'])

    #db = pymysql.connect("localhost", "root", "toor", "login_page")
    #db = pymysql.connect("localhost", "root", "toor", "login_page")
    #cursor = db.cursor()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    #print("db >>>>>>>>>>>>")
    #print(db)
    return cursor


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        print("inside login >>>>>>>>>>>>")
        # Create variables for easy access
        username = request.form['username']
        print("username >>>>>>>>>>>>>>>>>>>>>>>>")
        print(username)
        password = request.form['password']
        print("password >>>>>>>>>>>>>>>>>>>>>>>>")
        print(password)
        # Check if account exists using MySQL
        #cursor = db_connection()
        #cursor.execute('SELECT * FROM user_credentials WHERE username = %s AND password = MD5(%s)', (username, password))
        # Fetch one record and return result
        #user_credentials = cursor.fetchone()
        # If account exists in accounts table in out database
        #if user_credentials:
            # Create session data, we can access this data in other routes
        #    session['loggedin'] = True
        #    session['user_id'] = user_credentials['user_id']
        #    session['username'] = user_credentials['username']
            # Redirect to home page
        #    return 'Logged in successfully!'
        #else:
            # Account doesnt exist or username/password incorrect
        #    msg = 'Incorrect username/password!'
    return render_template('login.html', msg='')


# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
#@app.route('/register', methods=['GET', 'POST'])
@app.route('/register', methods=['POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    #if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
    if request.method == 'POST' and 'name' in request.form and 'phone' in request.form and 'email' in request.form:
        print("inside register >>>>>>>>>>>>>>>")
        userid = request.form['userid']
        # Create variables for easy access
        username = request.form['name']
        print("Username - " + username)
        phone = request.form['phone']
        print("phone - " + phone)
        email = request.form['email']
        print("email - " + email)
        password = request.form['password']
        conf_password = request.form['conf_password']
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)


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
        #cursor.execute('INSERT INTO user_credentials VALUES (NULL, %s, %s, %s)', (username, password, email,))
        cursor.execute('INSERT INTO user_credentials VALUES (%s, %s, %s, %s)', (userid, username, password, email,))
        mysql.connection.commit()
        msg = 'You have successfully registered!'




    return render_template('login.html', msg=msg)
    #return render_template('mohit.html', msg=msg)




@app.route('/administration', methods=['POST', 'GET'])
def administration():
    return "Administration section"

if __name__ == '__main__':
    app.run()
