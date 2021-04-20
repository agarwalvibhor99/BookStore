# https://codeshack.io/login-system-python-flask-mysql/#packages


from flask import Flask, render_template, request, url_for, session, redirect, jsonify
from flask_uuid import FlaskUUID
import sqlite3 as sql
import re
import datetime
import uuid


app = Flask(__name__)
FlaskUUID(app)
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
                'SELECT * FROM Manager WHERE username = ?', (username,))
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
                    'INSERT INTO Customer(username, password, firstName, lastName, phone, address, trustCount) VALUES (?, ?, ?, ?, ?, ?, ?)', (username, password, firstName, lastName, phone, address, 0))
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


@app.route('/pythonlogin/addTrust', methods=['GET', 'POST'])
def addTrust():
    # print("request form", request.form['username'])
    if 'loggedin' in session and session['type'] == 0:
        msg = ''

        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'username' in request.form:

            # Create variables for easy access
            if request.form['username'] == session['username']:
                msg = "Can't mark yourself trusted"
                return render_template('home.html', msg=msg)
            fromUsername = session['username']
            toUsername = request.form['username']
            reqType = request.form['type']
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute(
                    "SELECT * FROM Customer WHERE username = ?", (toUsername,))
                customer = cursor.fetchone()
                if not customer:
                    msg = "Invalid Username"
                    return render_template('home.html', msg=msg)
                cursor.execute(
                    "SELECT * FROM Trust WHERE fromUsername = ? AND toUsername=?", (fromUsername, toUsername,))
                record = cursor.fetchone()
                if(record):
                    msg = "You have already marked the User"
                    return render_template('home.html', msg=msg)
                if(reqType == "trust"):
                    cursor.execute(
                        'UPDATE Customer SET trustCount = trustCount + 1 WHERE username = ?', (request.form['username'],))
                    cursor.execute(
                        "INSERT INTO Trust VALUES(?, ?, 1)", (fromUsername, toUsername,))
                    msg = "Successfuly marked Trusted"
                elif(reqType == "untrust"):
                    cursor.execute(
                        'UPDATE Customer SET trustCount = trustCount - 1 WHERE username = ?', (request.form['username'],))
                    cursor.execute(
                        "INSERT INTO Trust VALUES(?, ?, -1)", (fromUsername, toUsername,))
                    msg = "Successfuly marked Trusted"
                con.commit()

        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
            # print(request.form)

        return render_template('home.html', msg=msg)
        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/pythonlogin/displayAllBooks', methods=['GET', 'POST'])
def displayAllBooks():
    if 'loggedin' in session and (session['type'] == 1 or session['type'] == 0):
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'GET':
            criteria = request.args['criteria']
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute(
                    'SELECT bookData.*, Author.name,AVG(score) FROM bookData LEFT JOIN Author ON bookData.authorID = Author.authorID LEFT JOIN Review ON bookData.ISBN = Review.ISBN GROUP BY Review.ISBN ORDER BY ?', (criteria,))
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
        print("in if")
        msg = ''
        print(request.form)
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST':

            # Create variables for easy access
            print(request.form)
            # quantString = 'quantity' + ISBN
            # ISBN = request.form['ISBN']
            # # print("Request form", request.form)
            # quantString = 'quantity' + ISBN
            # quantity = request.form['quantity']

            # print("Quantity up", quantity)
            # not checking books added 0 from default
            # print("details book: ", name, ISBN, date, stock, price,
            #       subject, language, noOfPages, authorID, authorName, keyword)

            # Check if account exists using MySQL

            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                totalAmt = 0
                orderID = 0
                orderID = uuid.uuid1()
                for key in request.form:
                    cursor.execute(
                        'SELECT * FROM bookData WHERE ISBN = ?', (key,))
                    book = cursor.fetchone()
                    print("book info", book)
                    msg = "not enough quantity of book " + \
                        book[1] + " with ISBN " + key
                    # print("quantity when high", int(request.form[key]))
                    if(not request.form[key]):
                        continue
                    qty = int(request.form[key])
                    totalAmt += book[6]*qty
                    if(int(book[5]) < int(request.form[key])):
                        return render_template('home.html', msg=msg)
                    else:
                        newQuantity = book[5]-int(request.form[key])
                        cursor.execute(
                            'UPDATE bookData SET stock = ? WHERE ISBN=?', (newQuantity, key))
                        print("quantity updated")

                        username = session['username']

                        ISBN = key
                        unitPrice = book[6]
                        print("orderID, username, iSBN, qty: ",
                              (orderID, username, ISBN, qty))
                        cursor.execute(
                            'INSERT INTO orderItem(orderID, ISBN, quantity, unitPrice) VALUES (?, ?, ?, ?)', (orderID.hex, ISBN, qty, unitPrice))
                    # add keyword

                        msg = 'You have successfully added new Manager!'
                print(totalAmt)
                cursor.execute(
                    'INSERT INTO orders(orderID, username, totalAmt) VALUES (?, ?, ?)', (orderID.hex, session['username'], totalAmt))
                con.commit()
                orderID = 0
                totalAmt = 0
                # print(existingDict)
                # session['cartItem'] = {ISBN: quantity}

                # print("session", session['cartItem'])
                # ADD CODE TO CHECK QUANTITY
                # print(book)

                # If account exists show error and validation checks

        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
            # print(request.form)

        return redirect(url_for('createOrder'))
        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/pythonlogin/viewOrder')
def viewOrder():
    # Check if user is loggedin
    if 'loggedin' in session and session['type'] == 0:
        # User is loggedin show them the home page
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'GET':
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                username = session['username']
                # print("username session", session['username'])
                cursor.execute(
                    'SELECT * FROM orders WHERE username = ?', (username,))
                orders = cursor.fetchall()
                # print(orders)
                orderItem = []
                for order in orders:
                    # print("order inside for loop", order)
                    # print("order[0]", order[0])
                    cursor.execute(
                        'SELECT * FROM orderItem WHERE orderID = ?', (order[0],))
                    # print(cursor.fetchall())
                    orderItem.append(cursor.fetchall())
                # print("order", orders)
                # print("order items", orderItem)

                # If account exists show error and validation checks
                if not orders:
                    msg = "You haven't placed any order till now."
                    return render_template("home.html", msg=msg, username=session['username'])
                else:
                    # print("orders", orders)
                    # print("orderItem", orderItem)
                    return render_template('viewOrder.html', data=orders, username=session['username'])

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/pythonlogin/viewOrderDetail')
def viewOrderDetail():
    # Check if user is loggedin
    if 'loggedin' in session and session['type'] == 0:
        # User is loggedin show them the home page
        msg = ''
        orderID = request.args['orderID']
        totalAmt = request.args['totalAmt']
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'GET':

            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                username = session['username']

                # print("username session", session['username'])
                cursor.execute(
                    'SELECT * FROM orderItem WHERE orderID = ?', (orderID,))
                orderItem = cursor.fetchall()
                myList = []
                # print(type(orderItem))
                for item in orderItem:
                    cursor.execute(
                        'SELECT name FROM bookData WHERE ISBN = ?', (item[1],))
                    name = cursor.fetchone()
                    item = list(item)

                    name = list(name)
                    name = name[0]
                    myList.append(item)

                    item.append(name)

                    item = tuple(item)

                # If account exists show error and validation checks
                # print(orderItem)
                if not orderItem:
                    msg = "There is some problem"
                else:
                    return render_template('viewOrderDetail.html', data=myList, orderID=orderID, totalAmt=totalAmt, username=session['username'])

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/pythonlogin/addReview', methods=['GET', 'POST'])
def addReview():
    if 'loggedin' in session and session['type'] == 0:
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'ISBN' in request.form and 'score' in request.form:
            comment = ''
            # Create variables for easy access
            username = request.form['username']
            ISBN = request.form['ISBN']
            score = request.form['score']
            if 'comment' in request.form:
                comment = request.form['comment']
            # not checking books added 0 from default
            # print("details book: ", name, ISBN, date, stock, price,
            #       subject, language, noOfPages, authorID, authorName, keyword)

            # Check if account exists using MySQL
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute(
                    'SELECT * FROM bookData WHERE ISBN = ?', (ISBN,)
                )
                book = cursor.fetchone()
                if not book:
                    msg = "Enter a correct ISBN"
                cursor.execute(
                    'SELECT * FROM Review WHERE username = ? AND ISBN = ?', (username, ISBN,))
                review = cursor.fetchone()

                # If account exists show error and validation checks
                if review:
                    msg = 'Review already exists!'

                else:
                    # Account doesnt exists and the form data is valid, now insert new account into accounts table
                    if not comment:
                        cursor.execute(
                            'INSERT INTO Review(username, ISBN, date, score) VALUES (?, ?, ?, ?)', (username, ISBN, datetime.datetime.now(), score,))
                        # add keyword
                        con.commit()
                        msg = 'You have successfully added review!'
                    else:
                        cursor.execute(
                            'INSERT INTO Review(username, ISBN, date, score, comment) VALUES (?, ?, ?, ?, ?)', (username, ISBN, datetime.datetime.now(), score, comment,))
                        # add keyword
                        con.commit()
                        msg = 'You have successfully added review!'

        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
            print(request.form)

        return render_template('addReview.html', msg=msg, username=session['username'])
        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/pythonlogin/updateStock', methods=['GET', 'POST'])
def updateStock():
    if 'loggedin' in session and session['type'] == 1:
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'ISBN' in request.form and 'stock' in request.form:
            # Create variables for easy access
            ISBN = request.form['ISBN']
            stock = request.form['stock']
            # print("details book: ", name, ISBN, date, stock, price,
            #       subject, language, noOfPages, authorID, authorName, keyword)

            # Check if account exists using MySQL
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute(
                    'SELECT * FROM bookData WHERE ISBN = ?', (ISBN,))
                book = cursor.fetchone()

                # If account exists show error and validation checks
                if not book:
                    msg = "Book doesn't exists!"

                elif not ISBN or not stock:
                    msg = 'Please fill out the form!'
                else:
                    cursor.execute('UPDATE bookData SET stock = stock + ? WHERE ISBN = ?',
                                   (stock, ISBN,))
                    cursor.execute(
                        'UPDATE Manager SET booksAdded = booksAdded + ? WHERE username = ?', (stock, session['username'],))

                # add multiple author for
                # If author exists show error and validation checks

                    con.commit()
                    msg = 'You have successfully updated Inventory!'

        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
            print(request.form)

        return render_template('updateStock.html', msg=msg, username=session['username'])
        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/pythonlogin/displayReview')
def displayReview():
    # Check if user is loggedin
    if 'loggedin' in session and session['type'] == 0:
        # User is loggedin show them the home page
        msg = ''
        ISBN = request.args['ISBN']
        print("ISBN IN REVIEW IS:", ISBN)
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'GET':
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute(
                    'SELECT * FROM bookData WHERE ISBN = ?', (ISBN,))
                book = cursor.fetchone()

                # If account exists show error and validation checks
                if not book:
                    msg = 'Invalid ISBN'
                else:
                    cursor.execute(
                        'SELECT * FROM Review WHERE ISBN = ?', (ISBN,))
                    review = cursor.fetchall()
                    if not review:
                        msg = "New review for this book, you can add one"
                        return render_template("addReview.html", msg=msg)
                    print(review)
                    return render_template('displayReview.html', data=review, username=session['username'])

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/pythonlogin/displayTopReview')
def displayTopReview():
    # Check if user is loggedin
    if 'loggedin' in session and session['type'] == 0:
        # User is loggedin show them the home page
        msg = ''
        ISBN = request.args['ISBN']
        count = request.args['count']
        print("ISBN IN REVIEW IS:", ISBN)
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'GET':
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute(
                    'SELECT * FROM bookData WHERE ISBN = ?', (ISBN,))
                book = cursor.fetchone()

                # If account exists show error and validation checks
                if not book:
                    msg = 'Invalid ISBN'
                else:
                    cursor.execute(
                        'SELECT * FROM Review WHERE ISBN = ? ORDER BY usefulness DESC LIMIT ?', (ISBN, count,))
                    review = cursor.fetchall()
                    if not review:
                        msg = "New review for this book, you can add one"
                        return render_template("addReview.html", msg=msg)
                    print(review)
                    return render_template('displayReview.html', data=review, username=session['username'])

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@ app.route('/pythonlogin/markUsefull', methods=['GET', 'POST'])
def markUsefull():
    # Check if user is loggedin
    if 'loggedin' in session and session['type'] == 0:
        # User is loggedin show them the home page
        msg = ''
        a = []
        for keys in request.form:
            a.append(request.form[keys])
        #     print("Keys:", keys, "value:", request.form[keys])
        # print("a", a)

        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST':
            if(session['username'] == a[0]):
                msg = "Can't mark your own review"
                return render_template("home.html", msg=msg)
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute("SELECT * FROM Usefulness WHERE fromUsername = ? AND toUsername = ? AND ISBN = ? ",
                               (session['username'], a[0], a[1],))
                usefullness = cursor.fetchone()
                if(usefullness):
                    msg = "You have already marked this comment"
                    return render_template('home.html', msg=msg, username=session['username'])
                cursor = con.cursor()
                reqType = request.form['type']
                if(reqType == "veryUseful"):
                    cursor.execute("INSERT INTO Usefulness VALUES (?, ?, ?, ?)",
                                   (session['username'], a[0], a[1], 1,))
                    cursor.execute(
                        'UPDATE Review SET usefulness = usefulness + 1 WHERE username = ? AND ISBN = ?', (a[0], a[1],))
                elif(reqType == "useful"):
                    cursor.execute("INSERT INTO Usefulness VALUES (?, ?, ?, ?)",
                                   (session['username'], a[0], a[1], 0,))
                    # cursor.execute(
                    #     'UPDATE Review SET usefulness = usefulness + 1 WHERE username = ? AND ISBN = ?', (a[0], a[1],))
                elif(reqType == "notUseful"):
                    cursor.execute("INSERT INTO Usefulness VALUES (?, ?, ?, ?)",
                                   (session['username'], a[0], a[1], -1,))
                    cursor.execute(
                        'UPDATE Review SET usefulness = usefulness - 1 WHERE username = ? AND ISBN = ?', (a[0], a[1],))
                con.commit()
                return render_template('markUsefull.html', msg="usefulness marked")

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/pythonlogin/bookStatistics', methods=['GET', 'POST'])
def bookStatistics():
    if 'loggedin' in session and session['type'] == 1:
        # print('in here')
        msg = ''

        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'GET' and request.query_string:

            print(request.query_string)
            reqType = request.args['criteria']
            value = request.args['count']
            print(reqType, type(value))
            print("in get")
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                if (reqType == "quantity"):
                    print("in checking name")
                    cursor.execute(
                        "SELECT ISBN, SUM(quantity) AS qty FROM orderItem GROUP BY ISBN ORDER BY qty DESC LIMIT ?", (value,))
                    book = cursor.fetchall()
# add join with bookData
                elif (reqType == "author"):
                    cursor.execute(
                        "SELECT A.ISBN, Author.name, A.qty FROM (SELECT ISBN, sum(quantity) AS qty FROM orderItem GROUP BY ISBN) AS A INNER JOIN writtenBy ON A.ISBN=writtenBy.ISBN INNER JOIN Author on Author.authorID=writtenBy.authorID ORDER BY A.qty DESC LIMIT ?", (value,))
                    book = cursor.fetchall()

                elif (reqType == "publisher"):
                    cursor.execute(
                        "SELECT A.ISBN, A.qty, bookData.publisher FROM (SELECT ISBN, sum(quantity) AS qty FROM orderItem GROUP BY ISBN) AS A INNER JOIN bookData ON A.ISBN = bookData.ISBN ORDER BY A.qty DESC LIMIT ?", (value,))
                    book = cursor.fetchall()

                # If account exists show error and validation checks
                if not book:
                    msg = 'There are no books in the store with this name!'
                    return render_template('home.html', msg=msg)
                else:
                    print(book)
                    return render_template('bookStatistics.html', data=book, username=session['username'])
        else:
            return render_template('bookStatistics.html', username=session['username'])
        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/pythonlogin/userAward', methods=['GET', 'POST'])
def userAward():
    if 'loggedin' in session and session['type'] == 1:
        # print('in here')
        msg = ''

        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'GET' and request.query_string:

            print(request.query_string)
            reqType = request.args['criteria']
            value = request.args['count']
            print(reqType, type(value))
            print("in get")
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                if (reqType == "trust"):
                    print("in checking name")
                    cursor.execute(
                        "SELECT * FROM Customer ORDER BY trustCount DESC LIMIT ?", (value,))
                    data = cursor.fetchall()

                elif (reqType == "useful"):
                    cursor.execute(
                        "SELECT username, SUM(usefulness) FROM Review GROUP BY username ORDER BY SUM(usefulness) DESC LIMIT ?", (value,))
                    data = cursor.fetchall()

                # If account exists show error and validation checks
                if not data:
                    msg = 'There are no books in the store with this name!'
                    return render_template('home.html', msg=msg)
                else:
                    print(data)
                    return render_template('userAward.html', data=data, username=session['username'])
        else:
            return render_template('userAward.html', username=session['username'])
        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
