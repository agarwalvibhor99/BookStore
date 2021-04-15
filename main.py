from flask import Flask, render_template, request, url_for, session, redirect
import sqlite3 as sql
import re
import datetime
app = Flask(__name__)
app.secret_key = '123456'


@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # return render_template('index.html', msg='')
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        with sql.connect("Book.db") as con:
            cur = con.cursor()
            cur.execute(
                'SELECT * FROM Customer WHERE username = ? AND password = ?', (username, password,))
            accountCustomer = cur.fetchone()
            print("username, password", (username, password))
            cur.execute(
                'SELECT * FROM Manager WHERE username = ? AND password = ?', (username, password,))
            accountManager = cur.fetchone()
            # print("username, password", (username, password))
            print("Account Manager: ", accountManager)
            print("Account Customer:", accountCustomer)
            # print("Account is", account)
            # print("Session is:", session['id'])
            if accountCustomer:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                # session['id'] = account['username']
                session['username'] = accountCustomer[0]
                session['type'] = 0
                # Redirect to home page
                return redirect(url_for('home'))
            elif accountManager:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                # session['id'] = account['username']
                session['username'] = accountManager[0]
                session['type'] = 1
                # Redirect to home page
                return redirect(url_for('managerhome'))
            else:
                # Account doesnt exist or username/password incorrect
                msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

# http://localhost:5000/python/logout - this will be the logout page


@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests


@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'firstName' in request.form and 'lastName' in request.form and 'address' in request.form and 'phone' in request.form:
        # Create variables for easy access
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        phone = request.form['phone']
        address = request.form['address']
        username = request.form['username']
        password = request.form['password']
        # print(firstName, lastName, phone, address, username, password)

        # Check if account exists using MySQL
        with sql.connect("Book.db") as con:
            cursor = con.cursor()
            cursor.execute(
                'SELECT * FROM Customer WHERE username = ?', (username,))
            accountCustomer = cursor.fetchone()
            cursor.execute(
                'SELECT * FROM Manger WHERE username = ?', (username,))
            accountManager = cursor.fetchone()
            # If account exists show error and validation checks
            if accountCustomer or accountManager:
                msg = 'Account already exists!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not username or not password or not phone or not address or not firstName or not lastName:
                msg = 'Please fill out the form!'
            else:
                # Account doesnt exists and the form data is valid, now insert new account into accounts table
                cursor.execute(
                    'INSERT INTO Customer(username, password, firstName, lastName, phone, address) VALUES (?, ?, ?, ?, ?, ?)', (username, password, firstName, lastName, phone, address))
                con.commit()
                msg = 'You have successfully registered!'

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session and session['type'] == 0:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/managerhome - this will be the home page, only accessible for loggedin users


@app.route('/pythonlogin/managerhome')
def managerhome():
    # Check if user is loggedin
    if 'loggedin' in session and session['type'] == 1:
        # User is loggedin show them the home page
        return render_template('managerhome.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users


@app.route('/pythonlogin/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = con.cursor()
        cursor.execute('SELECT * FROM accounts WHERE id = %s',
                       (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
