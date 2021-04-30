# https://codeshack.io/login-system-python-flask-mysql/#packages


from flask import Flask, render_template, request, url_for, session, redirect, jsonify
from flask_uuid import FlaskUUID
import sqlite3 as sql
import re
import datetime
from datetime import timedelta
import uuid
from flask_bcrypt import Bcrypt

app = Flask(__name__)
FlaskUUID(app)
app.secret_key = '123456'
bcrypt = Bcrypt(app)


@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # return render_template('index.html', msg='')
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        # password = bcrypt.generate_password_hash(password).decode('UTF-8')
        with sql.connect("Book.db") as con:
            cur = con.cursor()
            cur.execute(
                'SELECT username, password FROM Customer WHERE username = ?', (username,))
            accountCustomer = cur.fetchone()
            # print(accountCustomer[0])
            # accountCustomer = accountCustomer[0]
            # print(accountCustomer[1])
            authCustomer = False
            authManager = False
            if accountCustomer:
                storedPassword = str(accountCustomer[1])
                print(storedPassword)
                authCustomer = bcrypt.check_password_hash(
                    storedPassword, password)
            # print("username, password", (username, password))
            cur.execute(
                'SELECT username, password FROM Manager WHERE username = ?', (username,))
            accountManager = cur.fetchone()
            if accountManager:
                print(accountManager)
                storedPassword = str(accountManager[1])
                authManager = bcrypt.check_password_hash(
                    storedPassword, password)
            # print("username, password", (username, password))
            print("Account Manager: ", accountManager)
            print("Account Customer:", accountCustomer)
            # print("Account is", account)
            # print("Session is:", session['id'])
            cartItem = {}
            if authCustomer:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                # session['id'] = account['username']
                session['username'] = accountCustomer[0]
                session['type'] = 0
                session['cartItem'] = cartItem
                # Redirect to home page
                return redirect(url_for('home'))
            elif authManager:
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


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests


@app.route('/register', methods=['GET', 'POST'])
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
        password = bcrypt.generate_password_hash(password).decode('UTF-8')
        # Check if account exists using MySQL
        with sql.connect("Book.db") as con:
            cursor = con.cursor()
            cursor.execute(
                'SELECT * FROM Customer WHERE username = ?', (username,))
            accountCustomer = cursor.fetchone()
            cursor.execute(
                'SELECT * FROM Manager WHERE username = ?', (username,))
            accountManager = cursor.fetchone()
            # encrpyt password
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
@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session and session['type'] == 0:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    elif 'loggedin' in session and session['type'] == 1:
        return render_template('managerhome.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/managerhome - this will be the home page, only accessible for loggedin users


@app.route('/managerhome')
def managerhome():
    # Check if user is loggedin
    if 'loggedin' in session and session['type'] == 1:
        # User is loggedin show them the home page
        return render_template('managerhome.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/newBook', methods=['GET', 'POST'])
def newBook():
    if 'loggedin' in session and session['type'] == 1:
        msg = ''
        count = 0
        print(request.form)
        # To take care of multiple author
        for key in request.form:
            count += 1
        print("numbner of keys", count)
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'name' in request.form and 'ISBN' in request.form and 'date' in request.form and 'publisher' in request.form and 'stock' in request.form and 'price' in request.form and 'subject' in request.form and 'language' in request.form and 'noOfPages' in request.form and 'authorName' in request.form:
            # Create variables for easy access
            name = request.form['name']
            ISBN = request.form['ISBN']
            date = request.form['date']
            stock = request.form['stock']
            price = request.form['price']
            subject = request.form['subject']
            language = request.form['language']
            noOfPages = request.form['noOfPages']
            # authorID = request.form['authorID']
            authorName = request.form['authorName']
            keyword = request.form['keyword']
            publisher = request.form['publisher']
            authorCount = request.form['authorCount']
            keywordCount = request.form['keywordCount']

            finalISBN = "ISBN" + ISBN

            date = date.split("-")
            year, month, date = [int(x) for x in date]
            print(year, month, date)
            date = datetime.datetime(year, month, date)
            # date = datetime.datetime(date[2], date[1], date[0])
            # print("details book: ", name, ISBN, date, stock, price,
            #       subject, language, noOfPages, authorID, authorName, keyword)

            # Check if account exists using MySQL
            # print(request.form['authorName'])

            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute(
                    'SELECT * FROM bookData WHERE ISBN = ?', (finalISBN,))
                book = cursor.fetchone()

                # If account exists show error and validation checks
                if book:
                    msg = 'Book already exists!'

                elif not name or not ISBN or not date or not stock or not price or not subject or not language or not noOfPages or not authorName or not keyword or not publisher:
                    msg = 'Please fill out the form!'
                else:
                    cursor.execute(
                        'SELECT * FROM requestedBook WHERE ISBN = ?', (finalISBN,))
                    requested = cursor.fetchone()

                    if(requested):
                        cursor.execute(
                            'DELETE FROM requestedBook WHERE ISBN=?', (finalISBN,))

                    # Account doesnt exists and the form data is valid, now insert new account into accounts table
                    cursor.execute(
                        'INSERT INTO bookData(ISBN, name, language, publisher, date, stock, price, subject, noOfPages) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (finalISBN, name, language, publisher, date, stock, price, subject, noOfPages,))

                    cursor.execute(
                        'SELECT authorID FROM Author WHERE name = ?', (authorName,))
                    print("Author Name,", authorName)
                    author = cursor.fetchone()
                    print("author", author)
                    print(author)
                    authorID = author
                    if not author:
                        print("Author Not Found")
                        cursor.execute(
                            'INSERT INTO Author(name) VALUES (?)', (authorName,))
                        cursor.execute(
                            'SELECT authorID FROM Author WHERE name = ?', (authorName,))
                        authorID = cursor.fetchone()

                    cursor.execute(
                        'INSERT INTO writtenBy(ISBN, authorID) VALUES (?, ?)', (finalISBN, authorID[0],))
                # add multiple author for
                # If author exists show error and validation checks

                    authorCount = int(float(authorCount))
                    if authorCount > 1:
                        for i in range(1, authorCount):
                            # authorID = "authorID" + str(i)
                            authorName = "authorName" + str(i)
                            # authorID = request.form[authorID]
                            authorName = request.form[authorName]
                            print(authorName)
                            cursor.execute(
                                'SELECT authorID FROM Author WHERE name = ?', (authorName,))
                            author = cursor.fetchone()
                            if not author:
                                cursor.execute(
                                    'INSERT INTO Author(name) VALUES (?)', (authorName,))
                                cursor.execute(
                                    'SELECT authorID FROM Author WHERE name = ?', (authorName,))
                                authorID = cursor.fetchone()
                            cursor.execute(
                                'INSERT INTO writtenBY(ISBN, authorID) VALUES (?, ?)', (finalISBN, authorID[0],))

                    cursor.execute(
                        'SELECT keywordID FROM Keyword WHERE name = ?', (keyword,))
                    keywordID = cursor.fetchone()
                # add multiple author for
                # If author exists show error and validation checks
                    if not keywordID:
                        cursor.execute(
                            'INSERT INTO Keyword(name) VALUES (?)', (keyword,))
                        cursor.execute(
                            'SELECT keywordID FROM Keyword WHERE name = ?', (keyword,))
                        keywordID = cursor.fetchone()
                    #     cursor.execute('SELECT * FROM Keyword')
                    #     test = cursor.fetchall()
                    #     print("Test: ", test)
                    # print("line 252:", finalISBN, keywordID,
                    #       type(keywordID), keywordID[0])
                    cursor.execute(
                        'INSERT INTO containKeyword(ISBN, keywordID) VALUES (?, ?)', (finalISBN, keywordID[0],))
                    keywordCount = int(float(keywordCount))
                    if keywordCount > 1:
                        for i in range(1, keywordCount):
                            keyword = "keyword" + str(i)

                            keyword = request.form[keyword]
                            print(keyword)

                            cursor.execute(
                                'SELECT keywordID FROM Keyword WHERE name = ?', (keyword,))
                            keywordID = cursor.fetchone()
                            # add multiple author for
                            # If author exists show error and validation checks
                            if not keywordID:
                                cursor.execute(
                                    'INSERT INTO Keyword(name) VALUES (?)', (keyword,))
                                cursor.execute(
                                    'SELECT keywordID FROM Keyword WHERE name = ?', (keyword,))
                                keywordID = cursor.fetchone()

                            cursor.execute(
                                'INSERT INTO containKeyword(ISBN, keywordID) VALUES (?, ?)', (finalISBN, keywordID[0],))

                    con.commit()
                    msg = 'You have successfully added Book!'

        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
            print(request.form)

        return render_template('newBook.html', msg=msg, username=session['username'])
        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@ app.route('/newManager', methods=['GET', 'POST'])
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
            password = bcrypt.generate_password_hash(password).decode('UTF-8')

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
@app.route('/profile')
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
            print(account)
            if session['type'] == 1:
                return render_template('managerProfile.html', account=account)
            return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# Display all books
# add for managers option there


@app.route('/addTrust', methods=['GET', 'POST'])
def addTrust():
    # print("request form", request.form['username'])
    if 'loggedin' in session and session['type'] == 0:
        msg = ''
        print(request)
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'username' in request.form:

            if request.form['username'] == session['username']:
                msg = "Can't mark yourself trusted"
                return render_template('home.html', msg=msg, username=session['username'])
            fromUsername = session['username']
            toUsername = request.form['username']
            reqType = request.form['type']
            print(fromUsername, toUsername, reqType)
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute(
                    "SELECT * FROM Customer WHERE username = ?", (toUsername,))
                customer = cursor.fetchone()
                if not customer:
                    # print("if not customer")
                    msg = "Invalid Username"
                    return render_template('home.html', msg=msg, username=session['username'])
                # print("Checking")
                cursor.execute(
                    "SELECT * FROM Trust WHERE fromUsername = ? AND toUsername=?", (fromUsername, toUsername,))
                record = cursor.fetchone()
                print('record', record)
                # print((record[2] == 1 and reqType == "Trust")
                #   or record[2] == 0 and reqType == "Not Trusted")
                if((record and record[2] == 1 and reqType == "Trust") or (record and record[2] == -1 and reqType == "Not Trusted")):
                    msg = "You have already marked the User"
                    return render_template('home.html', msg=msg, username=session['username'])
                elif record:
                    if reqType == "Trust":
                        cursor.execute(
                            'UPDATE Customer SET trustCount = trustCount + 2 WHERE username = ?', (request.form['username'],))
                        cursor.execute(
                            "UPDATE Trust SET trustScore = 1 WHERE fromUsername = ? AND toUsername = ?", (fromUsername, toUsername,))
                        msg = "Successfuly updated to Trusted"
                    elif reqType == "Not Trusted":
                        cursor.execute(
                            'UPDATE Customer SET trustCount = trustCount -2 WHERE username = ?', (request.form['username'],))
                        cursor.execute(
                            "UPDATE Trust SET trustScore = -1 WHERE fromUsername = ? AND toUsername = ?", (fromUsername, toUsername,))
                        msg = "Successfuly updated to Not Trusted"

                elif(reqType == "Trust"):
                    cursor.execute(
                        'UPDATE Customer SET trustCount = trustCount + 1 WHERE username = ?', (request.form['username'],))
                    cursor.execute(
                        "INSERT INTO Trust VALUES(?, ?, 1)", (fromUsername, toUsername,))
                    msg = "Successfuly marked Trusted"
                elif(reqType == "Not Trusted"):
                    cursor.execute(
                        'UPDATE Customer SET trustCount = trustCount - 1 WHERE username = ?', (request.form['username'],))
                    cursor.execute(
                        "INSERT INTO Trust VALUES(?, ?, -1)", (fromUsername, toUsername,))
                    msg = "Successfuly marked Trusted"
                con.commit()
                print(msg)
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
            # print(request.form)

        return render_template('home.html', msg=msg, username=session['username'])
        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/displayAllBooks', methods=['GET', 'POST'])
def displayAllBooks():
    if 'loggedin' in session and (session['type'] == 1 or session['type'] == 0):
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'GET':
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor = con.cursor()
                cursor.execute("SELECT bookData.*, AVG(score) FROM bookData LEFT JOIN (SELECT Author.authorID, name, ISBN FROM writtenBy LEFT JOIN Author ON writtenBy.authorID=Author.authorID) AS A ON bookData.ISBN=A.ISBN LEFT JOIN Review ON bookData.ISBN = Review.ISBN GROUP BY bookData.ISBN  ORDER BY bookData.date")
                book = cursor.fetchall()
                # cursor.execute(
                #     'SELECT bookData.*, Author.name,AVG(score) FROM bookData LEFT JOIN Author ON bookData.authorID = Author.authorID LEFT JOIN Review ON bookData.ISBN = Review.ISBN GROUP BY Review.ISBN')
                # book = cursor.fetchall()

                # If account exists show error and validation checks
                if not book:
                    msg = 'There are no books in the store!'
                else:
                    print(book)
                    return render_template('displayAllBooks.html', data=book, username=session['username'])

        # elif request.method == 'GET' and request.args['criteria']:
        #     criteria = request.args['criteria']
        #     with sql.connect("Book.db") as con:
        #         cursor = con.cursor()
        #         cursor.execute("SELECT bookData.*, AVG(score) FROM bookData LEFT JOIN (SELECT Author.authorID, name, ISBN FROM writtenBy LEFT JOIN Author ON writtenBy.authorID=Author.authorID) AS A ON bookData.ISBN=A.ISBN LEFT JOIN Review ON bookData.ISBN = Review.ISBN GROUP BY bookData.ISBN  ORDER BY bookData.date")
        #         book = cursor.fetchall()
        #         # cursor.execute(
        #         #     'SELECT bookData.*, Author.name,AVG(score) FROM bookData LEFT JOIN Author ON bookData.authorID = Author.authorID LEFT JOIN Review ON bookData.ISBN = Review.ISBN GROUP BY Review.ISBN ORDER BY ?', (criteria,))
        #         # book = cursor.fetchall()

        #         # If account exists show error and validation checks
        #         if not book:
        #             msg = 'There are no books in the store!'
        #         else:
        #             print(book)
        #             return render_template('displayAllBooks.html', data=book, username=session['username'])

        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/displayBookQuery', methods=['GET', 'POST'])
def displayBookQuery():
    if 'loggedin' in session and (session['type'] == 1 or session['type'] == 0):
        # print('in here')
        msg = ''
        print(request.query_string)
        author = request.args['author']
        name = request.args['name']
        publisher = request.args['publisher']
        language = request.args['language']
        reqType = request.args['criteria']
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'GET':
            print("in get")
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                if (reqType == "date"):
                    if not name and not author and not publisher and not language:
                        cursor.execute(
                            "SELECT bookData.*, AVG(score) FROM bookData LEFT JOIN (SELECT Author.authorID, name, ISBN FROM writtenBy LEFT JOIN Author ON writtenBy.authorID=Author.authorID) AS A ON bookData.ISBN=A.ISBN LEFT JOIN Review ON bookData.ISBN = Review.ISBN GROUP BY bookData.ISBN  ORDER BY bookData.date")
                        book = cursor.fetchall()
                    else:
                        if not name:
                            name = "%"
                        if not author:
                            author = "%"
                        if not publisher:
                            publisher = "%"
                        if not language:
                            language = "%"
                        cursor.execute(
                            "SELECT bookData.*, AVG(score), A.name AS author FROM bookData LEFT JOIN (SELECT Author.authorID, name, ISBN FROM writtenBy LEFT JOIN Author ON writtenBy.authorID=Author.authorID) AS A ON bookData.ISBN=A.ISBN LEFT JOIN Review ON bookData.ISBN = Review.ISBN WHERE bookData.name like ? AND publisher like ? AND language like ? AND author like ? GROUP BY bookData.ISBN ORDER BY bookData.date", (name, publisher, language, author,))
                        book = cursor.fetchall()
                elif (reqType == "AVG(score)"):
                    if not name and not author and not publisher and not language:
                        cursor.execute(
                            "SELECT bookData.*, AVG(score) FROM bookData LEFT JOIN (SELECT Author.authorID, name, ISBN FROM writtenBy LEFT JOIN Author ON writtenBy.authorID=Author.authorID) AS A ON bookData.ISBN=A.ISBN LEFT JOIN Review ON bookData.ISBN = Review.ISBN GROUP BY bookData.ISBN  ORDER BY AVG(score) DESC")
                        book = cursor.fetchall()
                    else:
                        if not name:
                            name = "%"
                        if not author:
                            author = "%"
                        if not publisher:
                            publisher = "%"
                        if not language:
                            language = "%"
                        cursor.execute(
                            "SELECT bookData.*, AVG(score), A.name AS author FROM bookData LEFT JOIN (SELECT Author.authorID, name, ISBN FROM writtenBy LEFT JOIN Author ON writtenBy.authorID=Author.authorID) AS A ON bookData.ISBN=A.ISBN LEFT JOIN Review ON bookData.ISBN = Review.ISBN WHERE bookData.name like ? AND publisher like ? AND language like ? AND author like ? GROUP BY bookData.ISBN ORDER BY AVG(score)", (name, publisher, language, author,))
                        book = cursor.fetchall()

                if (reqType == "trustCount"):
                    if not name and not author and not publisher and not language:
                        cursor.execute(
                            "SELECT bookData.*, AVG(score) FROM bookData LEFT JOIN (SELECT Author.authorID, name, ISBN FROM writtenBy LEFT JOIN Author ON writtenBy.authorID=Author.authorID) AS A ON bookData.ISBN=A.ISBN LEFT JOIN (SELECT * FROM Review where username IN (SELECT username FROM Customer WHERE trustCount>0)) AS R ON bookData.ISBN = R.ISBN GROUP BY bookData.ISBN ORDER BY AVG(score)")
                        book = cursor.fetchall()
                    else:
                        if not name:
                            name = "%"
                        if not author:
                            author = "%"
                        if not publisher:
                            publisher = "%"
                        if not language:
                            language = "%"
                        cursor.execute(
                            "SELECT bookData.*, AVG(score), A.name AS author FROM bookData LEFT JOIN (SELECT Author.authorID, name, ISBN FROM writtenBy LEFT JOIN Author ON writtenBy.authorID=Author.authorID) AS A ON bookData.ISBN=A.ISBN LEFT JOIN (SELECT * FROM Review where username IN (SELECT username FROM Customer WHERE trustCount>0)) AS R ON bookData.ISBN = R.ISBN WHERE bookData.name like ? AND publisher like ? AND language like ? AND author like ? GROUP BY bookData.ISBN ORDER BY AVG(score)", (name, publisher, language, author,))
                        book = cursor.fetchall()

                # elif (reqType == "publisher"):
                #     cursor.execute(
                #         "SELECT * FROM bookData WHERE publisher like ?", [value])
                #     book = cursor.fetchall()

                # elif (reqType == "language"):
                #     cursor.execute(
                #         "SELECT * FROM bookData WHERE language like ?", [value])
                #     book = cursor.fetchall()

                # elif (reqType == "author"):
                #     cursor.execute(
                #         "SELECT * FROM bookData WHERE authorID = (SELECT authorID FROM Author WHERE name LIKE ?)", [value])
                #     book = cursor.fetchall()

                # If account exists show error and validation checks
                if not book:
                    msg = 'There are no books in the store with this name!'
                    return render_template('home.html', msg=msg, username=session['username'])
                else:
                    print(book)
                    return render_template('displayAllBooks.html', data=book, username=session['username'])

        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/createOrder')
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


@app.route('/addToCart', methods=['GET', 'POST'])
def addToCart():
    if 'loggedin' in session and session['type'] == 0:
        print("in if")
        msg = ''
        print(request.form)
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST':

            # Create variables for easy access
            # print(request.form)
            # print(request.form['submitType'])
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
                cursor.execute(
                    "SELECT balance FROM Customer WHERE username = ?", (session['username'],))
                balance = cursor.fetchone()
                if balance[0] < 0:
                    msg = "You have a Negative Balance. Please add credit to purchase book"
                    return render_template('home.html', msg=msg, username=session['username'])
                totalAmt = 0
                orderID = 0
                orderID = uuid.uuid1()
                for key in request.form:
                    cursor.execute(
                        'SELECT * FROM bookData WHERE ISBN = ?', (key,))
                    book = cursor.fetchone()
                    print("book info", book)
                    # msg = "not enough quantity of book " + \
                    #     book[1] + " with ISBN " + key
                    # print("quantity when high", int(request.form[key]))
                    if(not request.form[key]):
                        continue
                    qty = int(request.form[key])
                    totalAmt += book[6]*qty
                    if(int(book[5]) < int(request.form[key])):
                        msg = "not enough quantity of book " + \
                            book[1] + " with ISBN " + key
                        return render_template('home.html', msg=msg, username=session['username'])
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
                        cursor.execute('')
                        msg = 'Order successfully placed! Total Amount for your order is $' + \
                            str(totalAmt)
                print(totalAmt)
                cursor.execute(
                    'INSERT INTO orders(orderID, username, totalAmt, date) VALUES (?, ?, ?, ?)', (orderID.hex, session['username'], totalAmt, datetime.datetime.now(),))
                con.commit()
                orderID = 0
                totalAmt = 0
                # print(existingDict)
                # session['cartItem'] = {ISBN: quantity}

                # print("session", session['cartItem'])
                # ADD CODE TO CHECK QUANTITY
                # print(book)
                return render_template("home.html", msg=msg, username=session['username'])
                # If account exists show error and validation checks

        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
            # print(request.form)

        return redirect(url_for('createOrder'))
        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/viewOrder')
def viewOrder():
    # Check if user is loggedin
    if 'loggedin' in session and session['type'] == 0:
        # User is loggedin show them the home page
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'GET':
            print("in get")
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


@app.route('/viewOrderDetail')
def viewOrderDetail():
    # Check if user is loggedin
    if 'loggedin' in session and session['type'] == 0:
        # User is loggedin show them the home page
        msg = ''
        orderID = request.args['orderID']
        totalAmt = request.args['totalAmt']
        print(orderID, totalAmt)
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'GET':
            print("in get")
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


@app.route('/addReview', methods=['GET', 'POST'])
def addReview():
    if 'loggedin' in session and session['type'] == 0:
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'ISBN' in request.form and 'score' in request.form:
            comment = ''
            # Create variables for easy access
            username = request.form['username']
            ISBN = request.form['ISBN']
            ISBN = "ISBN"+ISBN
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


@app.route('/updateStock', methods=['GET', 'POST'])
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


@app.route('/displayReview')
def displayReview():
    # Check if user is loggedin
    if 'loggedin' in session and (session['type'] == 0 or session['type'] == 1):
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
                        return render_template("addReview.html", msg=msg, username=session["username"])
                    print(review)
                    return render_template('displayReview.html', data=review, username=session['username'])

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/displayTopReview')
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


@ app.route('/markUsefull', methods=['GET', 'POST'])
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
                return render_template("home.html", msg=msg, username=session['username'])
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


@app.route('/bookStatistics', methods=['GET', 'POST'])
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
                    # not sending ISBN to get rid of ISBN Column form front end
                    cursor.execute(
                        "SELECT name, SUM(quantity) AS qty FROM orderItem INNER JOIN bookData on orderItem.ISBN = bookData.ISBN GROUP BY orderItem.ISBN ORDER BY qty DESC LIMIT ?", (value,))
                    book = cursor.fetchall()
                elif (reqType == "author"):
                    cursor.execute(
                        "SELECT Author.name, A.qty FROM (SELECT ISBN, sum(quantity) AS qty FROM orderItem GROUP BY ISBN) AS A INNER JOIN writtenBy ON A.ISBN=writtenBy.ISBN INNER JOIN Author on Author.authorID=writtenBy.authorID ORDER BY A.qty DESC LIMIT ?", (value,))
                    book = cursor.fetchall()

                elif (reqType == "publisher"):
                    cursor.execute(
                        "SELECT bookData.publisher, A.qty FROM (SELECT ISBN, sum(quantity) AS qty FROM orderItem GROUP BY ISBN) AS A INNER JOIN bookData ON A.ISBN = bookData.ISBN ORDER BY A.qty DESC LIMIT ?", (value,))
                    book = cursor.fetchall()

                # If account exists show error and validation checks
                if not book:
                    msg = 'There are no books in the store with this name!'
                    return render_template('home.html', msg=msg, username=session['username'])
                else:
                    print(book)
                    return render_template('bookStatistics.html', data=book, username=session['username'])
        else:
            return render_template('bookStatistics.html', username=session['username'])
        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/userAward', methods=['GET', 'POST'])
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
                    return render_template('home.html', msg=msg, username=session['username'])
                else:
                    print(data)
                    return render_template('userAward.html', data=data, username=session['username'])
        else:
            return render_template('userAward.html', username=session['username'])
        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/updateProfile', methods=['GET', 'POST'])
def updateProfile():
    # print("request form", request.form['username'])
    if 'loggedin' in session and (session['type'] == 0 or session['type'] == 1):
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and ('phone' in request.form or 'address' in request.form or 'password' in request.form):

            # Create variables for easy access
            phone = request.form['phone']
            address = request.form['address']
            password = request.form['password']
            if password:
                password = bcrypt.generate_password_hash(
                    password).decode('UTF-8')

            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                if phone:
                    cursor.execute(
                        "UPDATE Customer SET phone=? WHERE username=?", (phone, session['username']))

                if address:
                    cursor.execute(
                        "UPDATE Customer SET address=? WHERE username=?", (address, session['username']))

                if password:
                    cursor.execute(
                        "UPDATE Customer SET password=? WHERE username=?", (password, session['username']))

                msg = "Successfuly updated the profile"
                con.commit()
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
            # print(request.form)

        return render_template('updateProfile.html', msg=msg, username=session['username'])
        # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# for customer


@app.route('/requestNewBook', methods=['GET', 'POST'])
def requestNewBook():
    if 'loggedin' in session and session['type'] == 0:
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'name' in request.form and 'ISBN' in request.form and 'publisher' in request.form and 'language' in request.form:
            # Create variables for easy access
            name = request.form['name']
            ISBN = request.form['ISBN']
            language = request.form['language']
            publisher = request.form['publisher']

            finalISBN = "ISBN" + ISBN

            # print("details book: ", name, ISBN, date, stock, price,
            #       subject, language, noOfPages, authorID, authorName, keyword)

            # Check if account exists using MySQL
            # print(request.form['authorName'])

            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute(
                    'SELECT * FROM bookData WHERE ISBN = ?', (finalISBN,))
                book = cursor.fetchone()

                cursor.execute(
                    'SELECT * FROM requestedBook WHERE ISBN = ?', (finalISBN,))
                requested = cursor.fetchone()

                # If account exists show error and validation checks
                if book:
                    msg = 'Book already exists!'

                elif requested:
                    msg = "Book already requested!"

                elif not name or not ISBN or not language or not publisher:
                    msg = 'Please fill out the form!'
                else:
                    # Account doesnt exists and the form data is valid, now insert new account into accounts table
                    cursor.execute(
                        'INSERT INTO requestedBook(username, ISBN, name, language, publisher) VALUES (?, ?, ?, ?, ?)', (session['username'], finalISBN, name, language, publisher,))

                    # add keyword
                    con.commit()
                    msg = 'You have successfully requested the Book!'

        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
            print(request.form)

        return render_template('requestNewBook.html', msg=msg, username=session['username'])
        # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# for Manager


@app.route('/requestedBooks', methods=['GET', 'POST'])
def requestedBooks():
    if 'loggedin' in session and session['type'] == 1:
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'GET':
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute(
                    'SELECT * FROM requestedBook')
                book = cursor.fetchall()
                print(book)
                # If account exists show error and validation checks
                if not book:
                    print("hii in here")
                    msg = 'No Books requested!'
                    return render_template('managerhome.html', msg=msg,
                                           username=session['username'])
                else:
                    print(book)
                    return render_template('requestedBooks.html', data=book, username=session['username'])

        # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# route for user to request credit


@app.route('/requestNewCredit', methods=['GET', 'POST'])
def requestNewCredit():
    if 'loggedin' in session and session['type'] == 0:
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'amount' in request.form:
            # Create variables for easy access
            amount = request.form['amount']

            print(amount)
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute(
                    'SELECT * FROM requestedCredit WHERE username = ?', (session['username'],))
                creditRequest = cursor.fetchone()
                if creditRequest:
                    msg = "You already have a pending credit request."
                    print("request:", creditRequest)
                    return render_template('home.html', msg=msg, username=session['username'])
                else:
                    cursor.execute('INSERT INTO requestedCredit(date, username, amount) VALUES (?, ?, ?)', (
                        datetime.datetime.now(), session['username'], amount,))

                con.commit()
                msg = 'Request for credit submitted!'
                return render_template('home.html', msg=msg, username=session['username'])

    return redirect(url_for('login'))

# route for manager to accept credit


@app.route('/requestedNewCredit', methods=['GET', 'POST'])
def requestedNewCredit():
    if 'loggedin' in session and session['type'] == 1:
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'GET':
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute(
                    'SELECT * FROM requestedCredit')
                requests = cursor.fetchall()
                print(requests)
                # If account exists show error and validation checks
                if not requests:
                    msg = 'No Credit requested!'
                else:
                    return render_template('requestedCredit.html', data=requests, username=session['username'])
        if request.method == 'POST':
            status = request.form['status']
            username = request.form['username']
            amount = request.form['amount']
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                if status == "Approve":
                    cursor.execute(
                        "UPDATE Customer SET balance = balance + ? WHERE username = ?", (amount, username, ))
                    msg = "Balance for user updated"

                cursor.execute(
                    "DELETE FROM requestedCredit WHERE username = ?", (username, ))
                con.commit()
        return render_template('managerhome.html', msg=msg, username=session['username'])

        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/buyingSuggestion', methods=['GET', 'POST'])
def buyingSuggestion():
    if 'loggedin' in session and (session['type'] == 0):
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'GET':
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute('SELECT * FROM bookData WHERE ISBN IN (SELECT ISBN FROM (SELECT DISTINCT(ISBN) FROM orders LEFT JOIN orderItem on orders.orderID = orderItem.orderID WHERE username IN (SELECT DISTINCT(username) FROM orderItem LEFT JOIN orders ON orderItem.orderID=orders.orderID  WHERE ISBN in (SELECT ISBN from orders LEFT JOIN orderItem on orders.orderID = orderItem.orderID where username = ?))) AS A WHERE A.ISBN NOT IN (SELECT ISBN from orders LEFT JOIN orderItem on orders.orderID = orderItem.orderID where username =?))', (
                    session['username'], session['username'],))
                # cursor.execute('SELECT * FROM bookData WHERE ISBN IN (SELECT DISTINCT(ISBN) FROM (SELECT orderID from orderItem  WHERE ISBN in (SELECT ISBN from orders LEFT JOIN orderItem on orders.orderID = orderItem.orderID where username = ?)) AS A LEFT JOIN orderItem ON A.orderID = orderItem.orderID WHERE ISBN NOT IN (SELECT ISBN from orders LEFT JOIN orderItem on orders.orderID = orderItem.orderID where username = ?))',
                #                (session['username'], session['username'],))
                book = cursor.fetchall()

                # If account exists show error and validation checks
                if not book:
                    msg = 'Sorry! There are no suggested books in the store for you!'
                    return render_template('home.html', msg=msg, username=session['username'])
                else:
                    print(book)
                    return render_template('buyingSuggestion.html', data=book, username=session['username'])

        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/displayAuthor', methods=['GET', 'POST'])
def displayAuthor():
    if 'loggedin' in session and (session['type'] == 1 or session['type'] == 0):
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'GET':
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute(
                    'SELECT * FROM Author')
                author = cursor.fetchall()

                # If account exists show error and validation checks
                if not author:
                    msg = 'No Author Found!'
                else:
                    print(author)
                    return render_template('displayAuthor.html', data=author, username=session['username'])

        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/degreeSeparation', methods=['GET', 'POST'])
def degreeSeparation():
    if 'loggedin' in session and (session['type'] == 1 or session['type'] == 0):
        msg = ''
        authorID = request.args['authorID']
        degree = request.args['degree']
        if request.method == 'GET' and authorID and degree:
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                if degree == "onedegree":

                    cursor.execute(
                        'SELECT authorID, authorName FROM (SELECT ISBN, writtenBy.authorID, name AS authorName FROM writtenBy LEFT JOIN Author ON writtenBy.authorID = Author.authorID WHERE ISBN IN (SELECT ISBN FROM (SELECT ISBN FROM writtenBy WHERE authorID =?) AS A WHERE A.ISBN IN (SELECT ISBN FROM writtenBy GROUP BY ISBN ))) WHERE authorID != ?', (authorID, authorID,))
                    author = cursor.fetchall()
                    cursor.execute(
                        'SELECT * FROM bookData WHERE ISBN IN (SELECT ISBN FROM writtenBy WHERE authorID IN(SELECT authorID FROM (SELECT ISBN, writtenBy.authorID, name AS authorName FROM writtenBy LEFT JOIN Author ON writtenBy.authorID = Author.authorID WHERE ISBN IN (SELECT ISBN FROM (SELECT ISBN FROM writtenBy WHERE authorID =?) AS A WHERE A.ISBN IN (SELECT ISBN FROM writtenBy GROUP BY ISBN ))) WHERE authorID != ?))', (authorID, authorID,))
                    book = cursor.fetchall()
                    print(book)
                elif degree == "twodegree":
                    print("authorID", authorID)
                    cursor.execute('SELECT * FROM Author WHERE authorID IN (SELECT C.authorID FROM writtenBy AS C, writtenBy AS D WHERE D.authorID IN (SELECT authorID FROM (SELECT ISBN, writtenBy.authorID, name AS authorName FROM writtenBy LEFT JOIN Author ON writtenBy.authorID = Author.authorID WHERE ISBN IN (SELECT ISBN FROM (SELECT ISBN FROM writtenBy WHERE authorID =?) AS A WHERE A.ISBN IN (SELECT ISBN FROM writtenBy GROUP BY ISBN ))) WHERE authorID != ?) AND C.authorID NOT IN ((SELECT authorID FROM (SELECT ISBN, writtenBy.authorID, name AS authorName FROM writtenBy LEFT JOIN Author ON writtenBy.authorID = Author.authorID WHERE ISBN IN (SELECT ISBN FROM (SELECT ISBN FROM writtenBy WHERE authorID =?) AS A WHERE A.ISBN IN (SELECT ISBN FROM writtenBy GROUP BY ISBN ))) WHERE authorID != ?)) AND D.ISBN = C.ISBN AND C.authorID !=?)', (authorID, authorID, authorID, authorID, authorID,))
                    author = cursor.fetchall()
                    print("author:", author)
                    cursor.execute('SELECT * FROM bookData WHERE ISBN IN (SELECT ISBN FROM writtenBy WHERE authorID IN (SELECT C.authorID FROM writtenBy AS C, writtenBy AS D WHERE D.authorID IN (SELECT authorID FROM (SELECT ISBN, writtenBy.authorID, name AS authorName FROM writtenBy LEFT JOIN Author ON writtenBy.authorID = Author.authorID WHERE ISBN IN (SELECT ISBN FROM (SELECT ISBN FROM writtenBy WHERE authorID =?) AS A WHERE A.ISBN IN (SELECT ISBN FROM writtenBy GROUP BY ISBN ))) WHERE authorID != ?) AND C.authorID NOT IN ((SELECT authorID FROM (SELECT ISBN, writtenBy.authorID, name AS authorName FROM writtenBy LEFT JOIN Author ON writtenBy.authorID = Author.authorID WHERE ISBN IN (SELECT ISBN FROM (SELECT ISBN FROM writtenBy WHERE authorID =?) AS A WHERE A.ISBN IN (SELECT ISBN FROM writtenBy GROUP BY ISBN ))) WHERE authorID != ?)) AND D.ISBN = C.ISBN AND C.authorID !=?))', (authorID, authorID, authorID, authorID, authorID,))
                    book = cursor.fetchall()
                    print("book:", book)

                if not author:
                    msg = 'No Author Found!'
                    return render_template('home.html', msg=msg, username=session['username'])
                else:
                    print(author)
                    return render_template("separatedSuggestion.html", data=book, author=author, username=session['username'])
                    # return render_template('displayAuthor.html', data=author, username=session['username'])


@app.route('/cancelOrder', methods=['GET', 'POST'])
def cancelOrder():
    if 'loggedin' in session and session['type'] == 0:
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'GET':
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                lastDate = datetime.datetime.now() - timedelta(days=1)
                cursor.execute(
                    'SELECT orders.* FROM orders WHERE orders.username = ? AND orders.date>?', (session['username'], lastDate, ))
                order = cursor.fetchall()

                # If account exists show error and validation checks
                if not order:
                    msg = 'No order in past 1 day!'
                    return render_template('home.html', msg=msg, username=session['username'])
                else:
                    print(order)
                    return render_template('cancelOrder.html', data=order, username=session['username'])
        if request.method == 'POST':
            print("in Post")
            orderID = request.form['orderID']
            totalAmt = request.form['totalAmt']
            print("order, amt", orderID, totalAmt)
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute(
                    'UPDATE Customer SET balance = balance + ? WHERE username = ?', (totalAmt, session['username'],))
                cursor.execute(
                    'DELETE FROM orders WHERE orderID = ?', (orderID,))
                # on cascade not working
                cursor.execute(
                    'SELECT ISBN, quantity FROM orderItem WHERE orderID=?', (orderID,))
                items = cursor.fetchall()
                print(items)
                for item in items:
                    cursor.execute(
                        'UPDATE bookData SET stock = stock+? WHERE ISBN=?', (item[1], item[0]))

                # STILL UPDATE THE QUANTITY
                cursor.execute(
                    'DELETE FROM orderItem WHERE orderID = ?', (orderID,))

                con.commit()
            msg = "Order successfully cancelled and the amount is credited to your account"
            return render_template('home.html', msg=msg, username=session['username'])

        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/displayCustomer', methods=['GET', 'POST'])
def displayCustomer():
    if 'loggedin' in session and session['type'] == 1:
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'GET':
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute(
                    'SELECT * FROM Customer')
                customer = cursor.fetchall()

                # If account exists show error and validation checks
                if not customer:
                    msg = 'No Customer Registered!'
                else:
                    print(customer)
                    return render_template('displayCustomer.html', data=customer, username=session['username'])

        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/deleteCustomer', methods=['GET', 'POST'])
def deleteCustomer():
    # print("request form", request.form['username'])
    print('here in delete customer')
    if 'loggedin' in session and session['type'] == 0:
        msg = ''
        print(request)
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST':
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                print("inpost")
                cursor.execute(
                    "DELETE FROM Customer WHERE username = ?", (session['username'],))
                cursor.execute(
                    "UPDATE Review SET username='OLD USER' WHERE username = ?", (session['username'],))
                cursor.execute(
                    "UPDATE Trust SET fromUsername='OLD USER' WHERE fromUsername = ?", (session['username'],))
                cursor.execute(
                    "DELETE FROM Trust WHERE toUsername = ?", (session['username'],))
                cursor.execute(
                    "UPDATE Usefulness SET fromUsername='OLD USER' WHERE fromUsername = ?", (session['username'],))
                cursor.execute(
                    "DELETE FROM Usefulness WHERE toUsername = ?", (session['username'],))
                cursor.execute(
                    "SELECT orderID FROM orders WHERE username = ?", (session['username'],))
                orders = cursor.fetchall()
                if orders:
                    for order in orders:
                        print("orderID:", order)
                        cursor.execute(
                            "DELETE FROM orderItem WHERE orderID = ?", (order[0],))
                cursor.execute(
                    "DELETE FROM orders WHERE username = ?", (session['username'],))
                cursor.execute(
                    "DELETE FROM requestedBook WHERE username = ?", (session['username'],))
                cursor.execute(
                    "DELETE FROM requestedCredit WHERE username = ?", (session['username'],))
                msg = "All your Data has been removed from the Book Store System"
                con.commit()

        # User is not loggedin redirect to login page or data removed
    return redirect(url_for('login'))


@app.route('/bestEmployee', methods=['GET', 'POST'])
def bestEmployee():
    if 'loggedin' in session and session['type'] == 1:
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'GET':
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute(
                    'SELECT * FROM Manager GROUP BY username HAVING MAX(booksAdded)')
                manager = cursor.fetchall()

                # If account exists show error and validation checks

                return render_template('bestEmployee.html', data=manager, username=session['username'])

        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/addToCartRental', methods=['GET', 'POST'])
def addToCartRental():
    if 'loggedin' in session and session['type'] == 0:
        print("in if")
        msg = ''
        print(request.form)
        if request.method == 'POST':
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute(
                    "SELECT balance FROM Customer WHERE username = ?", (session['username'],))
                balance = cursor.fetchone()
                if balance[0] < 0:
                    msg = "You have a Negative Balance. Please add credit to purchase book"
                    return render_template('home.html', msg=msg, username=session['username'])
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
                    totalAmt += book[6]*qty*0.1
                    if(int(book[5]) < int(request.form[key])):
                        return render_template('home.html', msg=msg, username=session['username'])
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
                            'INSERT INTO rentalItem(orderID, ISBN, quantity, unitPrice) VALUES (?, ?, ?, ?)', (orderID.hex, ISBN, qty, unitPrice*.1))
                    # add keyword

                        msg = 'Order successfully placed! Total Amount for your order is $' + \
                            str(totalAmt)
                print(totalAmt)
                cursor.execute(
                    'INSERT INTO rentals(orderID, username, totalAmt, date) VALUES (?, ?, ?, ?)', (orderID.hex, session['username'], totalAmt, datetime.datetime.now(),))
                con.commit()
                orderID = 0
                totalAmt = 0
                # print(existingDict)
                # session['cartItem'] = {ISBN: quantity}

                # print("session", session['cartItem'])
                # ADD CODE TO CHECK QUANTITY
                # print(book)
                return render_template("home.html", msg=msg, username=session['username'])
                # If account exists show error and validation checks

        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
            # print(request.form)

        return redirect(url_for('createOrder'))
        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/createRental',  methods=['GET', 'POST'])
def createRental():
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
                    return render_template('createRental.html', data=book, username=session['username'])

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/returnRental',  methods=['GET', 'POST'])
def returnRental():
    # Check if user is loggedin
    if 'loggedin' in session and session['type'] == 0:
        # User is loggedin show them the home page
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'GET':
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute(
                    'SELECT * FROM rentals WHERE username=?', (session['username'],))
                rental = cursor.fetchall()

                # If account exists show error and validation checks
                if not rental:
                    msg = "You don't have any rentals"
                    return render_template("home.html", msg=msg, username=session['username'])
                else:
                    print(rental)
                    return render_template('returnRental.html', data=rental, username=session['username'])
        if request.method == 'POST':
            print("in Post")
            orderID = request.form['orderID']
            totalAmt = request.form['totalAmt']
            print("order, amt", orderID, totalAmt)
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                todayDate = datetime.datetime.now()

                cursor.execute(
                    'SELECT date, totalAmt FROM rentals WHERE orderID = ?', (orderID,))
                orderDate = cursor.fetchone()
                print(orderDate)
                if orderDate:
                    orderDate = orderDate[0]
                    print('orderData[1]', (totalAmt))
                    # totalAmt = float(orderDate[1])
                    print("total amt from table", totalAmt)
                    print("orderDate", orderDate)
                    orderDate = datetime.datetime.strptime(
                        orderDate, '%Y-%m-%d %H:%M:%S.%f')

                    # testDate = date = datetime.datetime(2021, 4, 1)
                    # print("test Date", testDate)
                    diff = (todayDate-orderDate).days
                    # diff = (todayDate - testDate).days
                    diff = float(diff)
                    print("difference:", diff)
                    penalty = 0
                    if diff > 7:
                        totalAmt *= 10
                        penalty = totalAmt * 0.5*(diff-7.0)
                        totalAmt = totalAmt*0.1 + penalty
                        print("total amt, penalty", totalAmt, penalty)
                        cursor.execute(
                            'UPDATE Customer SET balance = balance - ? WHERE username=?', (penalty, session['username'],))
                    cursor.execute(
                        'SELECT ISBN, quantity from rentalItem WHERE orderID = ?', (orderID,))
                    rentalItems = cursor.fetchall()
                    print(rentalItems)
                    for item in rentalItems:
                        cursor.execute(
                            'UPDATE bookData SET stock = stock+? WHERE ISBN=?', (item[1], item[0]))
                        # print(item[0])
                    cursor.execute(
                        'DELETE FROM rentals WHERE orderID = ?', (orderID,))
                    cursor.execute(
                        'DELETE FROM rentalItem WHERE orderID = ?', (orderID,))
                    # cursor.execute(
                    #     'UPDATE Customer SET balance = balance + ? WHERE username = ?', (totalAmt, session['username'],))
                    # cursor.execute(
                    #     'DELETE FROM orders WHERE orderID = ?', (orderID,))
                    # # on cascade not working
                    # cursor.execute(
                    #     'DELETE FROM orderItem WHERE orderID = ?', (orderID,))
                    con.commit()
                    if penalty:
                        msg = "Rental successfuly returned. The total amount charged is $" + \
                            str(totalAmt) + ". There is no Penalty."
                    else:
                        msg = "Rental successfuly returned. The total amount charged is $" + \
                            str(totalAmt) + \
                            " which includes a penalty of $" + str(penalty)

            return render_template('home.html', msg=msg, username=session['username'])

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/browseCustomerProfile', methods=['GET', 'POST'])
def browseCustomerProfile():
    if 'loggedin' in session and session['type'] == 0:
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'GET':
            with sql.connect("Book.db") as con:
                cursor = con.cursor()
                cursor.execute(
                    'SELECT * FROM Customer WHERE username != ?', (session['username'],))
                customer = cursor.fetchall()

                # If account exists show error and validation checks
                if not customer:
                    msg = 'No Customer Registered!'
                else:
                    print(customer)
                    return render_template('browseCustomerProfile.html', data=customer, username=session['username'])
        # if request.method == 'POST':
        #     username = request.form[username]
        #     trust = request.form[trust]
        #     print(username,)
        # User is not loggedin redirect to login page
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
