# https://codeshack.io/login-system-python-flask-mysql/#packages


from flask import Flask, render_template, request, url_for, session, redirect, jsonify
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
            cartItem = {}
            if accountCustomer:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                # session['id'] = account['username']
                session['username'] = accountCustomer[0]
                session['type'] = 0
                session['cartItem'] = cartItem
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


@app.route('/pythonlogin/newBook', methods=['GET', 'POST'])
def newBook():
    if 'loggedin' in session and session['type'] == 1:
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'name' in request.form and 'ISBN' in request.form and 'date' in request.form and 'publisher' in request.form and 'stock' in request.form and 'price' in request.form and 'subject' in request.form and 'language' in request.form and 'noOfPages' in request.form and 'authorID' in request.form and 'authorName' in request.form:
            # Create variables for easy access
            name = request.form['name']
            ISBN = request.form['ISBN']
            date = request.form['date']
            stock = request.form['stock']
            price = request.form['price']
            subject = request.form['subject']
            language = request.form['language']
            noOfPages = request.form['noOfPages']
            authorID = request.form['authorID']
            authorName = request.form['authorName']
            keyword = request.form['keyword']
            publisher = request.form['publisher']
            # print("details book: ", name, ISBN, date, stock, price,
            #       subject, language, noOfPages, authorID, authorName, keyword)

            # Check if account exists using MySQL
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute(
                    'SELECT * FROM bookData WHERE ISBN = ?', (ISBN,))
                book = cursor.fetchone()

                # If account exists show error and validation checks
                if book:
                    msg = 'Book already exists!'

                elif not name or not ISBN or not date or not stock or not price or not subject or not language or not noOfPages or not authorID or not authorName or not keyword or not publisher:
                    msg = 'Please fill out the form!'
                else:
                    # Account doesnt exists and the form data is valid, now insert new account into accounts table
                    cursor.execute(
                        'INSERT INTO bookData(ISBN, name, authorID, publisher, date, stock, price, subject, noOfPages) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (ISBN, name, authorID, publisher, date, stock, price, subject, noOfPages))
                    cursor.execute(
                        'SELECT * FROM Author WHERE authorID = ?', (authorID))
                    author = cursor.fetchone()
                # add multiple author for
                # If author exists show error and validation checks
                    if not author:
                        cursor.execute(
                            'INSERT INTO Author(authorID, name) VALUES (?, ?)', (authorID, name))
                    else:
                        cursor.execute(
                            'INSERT INTO writtenBY(ISBN, authorID) VALUES (?, ?)', (ISBN, authorID))
                    # add keyword
                    con.commit()
                    msg = 'You have successfully added Book!'

        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
            print(request.form)

        return render_template('newBook.html', msg=msg, username=session['username'])
        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/pythonlogin/newManager', methods=['GET', 'POST'])
def newManager():
    if 'loggedin' in session and session['type'] == 1:
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'firstName' in request.form and 'lastName' in request.form and 'phone' in request.form and 'address' in request.form and 'username' in request.form and 'password' in request.form and 'salary' in request.form:
            # Create variables for easy access
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            phone = request.form['phone']
            address = request.form['address']
            username = request.form['username']
            password = request.form['password']
            salary = request.form['salary']
            # not checking books added 0 from default
            # print("details book: ", name, ISBN, date, stock, price,
            #       subject, language, noOfPages, authorID, authorName, keyword)

            # Check if account exists using MySQL
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute(
                    'SELECT * FROM Manager WHERE username = ?', (username,))
                account = cursor.fetchone()

                # If account exists show error and validation checks
                if account:
                    msg = 'Manager already exists!'

                elif not firstName or not lastName or not username or not password or not phone or not address or not salary:
                    msg = 'Please fill out the form!'
                else:
                    # Account doesnt exists and the form data is valid, now insert new account into accounts table
                    cursor.execute(
                        'INSERT INTO Manager(username, password, firstName, lastName, phone, address, salary) VALUES (?, ?, ?, ?, ?, ?, ?)', (username, password, firstName, lastName, phone, address, salary))
                    # add keyword
                    con.commit()
                    msg = 'You have successfully added new Manager!'

        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
            print(request.form)

        return render_template('newManager.html', msg=msg, username=session['username'])
        # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users


# create one profile for maanger and other for customer
@app.route('/pythonlogin/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        with sql.connect("Book.db") as con:
            cursor = con.cursor()
            if(session['type'] == 1):
                cursor.execute('SELECT * FROM Manager WHERE username = ?',
                               (session['username'],))
                account = cursor.fetchone()
            else:
                cursor.execute('SELECT * FROM Customer WHERE username = ?',
                               (session['username'],))
                account = cursor.fetchone()
            # Show the profile page with account info
            return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# Display all books
# add for managers option there


@app.route('/pythonlogin/displayAllBooks', methods=['GET', 'POST'])
def displayAllBooks():
    if 'loggedin' in session and (session['type'] == 1 or session['type'] == 0):
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'GET':
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute(
                    'SELECT * FROM bookData')
                book = cursor.fetchall()

                # If account exists show error and validation checks
                if not book:
                    msg = 'There are no books in the store!'
                else:
                    print(book)
                    return render_template('displayAllBooks.html', data=book, username=session['username'])

        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/pythonlogin/displayBookQuery', methods=['GET', 'POST'])
def displayBookQuery():
    if 'loggedin' in session and (session['type'] == 1 or session['type'] == 0):
        # print('in here')
        msg = ''
        print(request.query_string)
        reqType = request.args['type']
        value = request.args['value']
        print(reqType, type(value))
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'GET':
            print("in get")
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                if (reqType == "name"):
                    print("in checking name")
                    cursor.execute(
                        "SELECT * FROM bookData WHERE name like ?", [value])
                    book = cursor.fetchall()

                elif (reqType == "publisher"):
                    cursor.execute(
                        "SELECT * FROM bookData WHERE publisher like ?", [value])
                    book = cursor.fetchall()

                elif (reqType == "language"):
                    cursor.execute(
                        "SELECT * FROM bookData WHERE language like ?", [value])
                    book = cursor.fetchall()

                elif (reqType == "author"):
                    cursor.execute(
                        "SELECT * FROM bookData WHERE authorID = (SELECT authorID FROM Author WHERE name LIKE ?)", [value])
                    book = cursor.fetchall()

                # If account exists show error and validation checks
                if not book:
                    msg = 'There are no books in the store with this name!'
                    return render_template('home.html', msg=msg)
                else:
                    print(book)
                    return render_template('displayAllBooks.html', data=book, username=session['username'])

        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/pythonlogin/createOrder')
def createOrder():
    # Check if user is loggedin
    if 'loggedin' in session and session['type'] == 0:
        # User is loggedin show them the home page
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'GET':
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute(
                    'SELECT * FROM bookData')
                book = cursor.fetchall()

                # If account exists show error and validation checks
                if not book:
                    msg = 'There are no books in the store!'
                else:
                    print(book)
                    return render_template('createOrder.html', data=book, username=session['username'])

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/pythonlogin/addToCart', methods=['GET', 'POST'])
def addToCart():
    if 'loggedin' in session and session['type'] == 0:
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'quantity' in request.form and 'ISBN' in request.form:
            # Create variables for easy access
            quantString = 'quantity' + ISBN
            ISBN = request.form['ISBN']
            # print("Request form", request.form)
            quantString = 'quantity' + ISBN
            quantity = request.form['quantity']
            # print("Quantity up", quantity)
            # not checking books added 0 from default
            # print("details book: ", name, ISBN, date, stock, price,
            #       subject, language, noOfPages, authorID, authorName, keyword)

            # Check if account exists using MySQL
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute(
                    'SELECT * FROM bookData WHERE ISBN = ?', (ISBN,))
                book = cursor.fetchone()
                existingDict = session['cartItem']
                # print(existingDict)
                session['cartItem'] = {ISBN: quantity}
                # print("session", session['cartItem'])
                # ADD CODE TO CHECK QUANTITY
                # print(book)

                # If account exists show error and validation checks

                if not quantity:
                    msg = 'Please fill out the quantity!'

        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
            # print(request.form)

        return redirect(url_for('createOrder'))
        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
