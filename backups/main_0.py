from flask import Flask, render_template, request, redirect, url_for, session
import configparser
import re
from mysql_query import *

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)

app.secret_key = 'loggedin'

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = db_connection()
        cursor.execute('SELECT * FROM user_credentials WHERE username = %s AND password = MD5(%s)', (username, password))
        # Fetch one record and return result
        user_credentials = cursor.fetchone()
        # If account exists in accounts table in out database
        if user_credentials:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['user_id'] = user_credentials['user_id']
            session['username'] = user_credentials['username']
            # Redirect to home page
            return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg='')

@app.route('/login/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/login/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        print("Username - " + username)
        password = request.form['password']
        print("password - " + password)
        email = request.form['email']
        print("email - " + email)
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

if __name__ == '__main__':
    app.run()
