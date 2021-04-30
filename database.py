import sqlite3

conn = sqlite3.connect('Book.db')

c = conn.cursor()
# c.execute('DROP Table containKeyword')
# c.execute('DROP Table orderItem')
# c.execute('DROP Table orders')
# c.execute('DROP Table Keyword')
# c.execute('DROP Table bookData')
# c.execute("DROP TABLE Author")
# c.execute("DROP TABLE writtenBy")
# c.execute("DROP TABLE rentals")
# c.execute("DELETE FROM rentalItem ")

c.execute("""CREATE TABLE IF NOT EXISTS Customer (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            phone INT NOT NULL,
            address TEXT NOT NULL,
            balance FLOAT DEFAULT 0,
            dateOfJoining DATETIME DEFAULT CURRENT_TIMESTAMP)""")

c.execute("""CREATE TABLE IF NOT EXISTS Manager (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            phone INT NOT NULL,
            address TEXT NOT NULL,
            salary FLOAT DEFAULT 0,
            booksAdded INT DEFAULT 0)""")

c.execute("""CREATE TABLE IF NOT EXISTS bookData (
            ISBN TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            language TEXT NOT NULL,
            publisher text NOT NULL,
            date DATETIME NOT NULL,
            stock INT NOT NULL,
            price float NOT NULL,
            subject TEXT NOT NULL,
            noOfPages INT NOT NULL
            )""")

c.execute("""CREATE TABLE IF NOT EXISTS writtenBy (
            ISBN TEXT NOT NULL,
            authorID INT NOT NULL
)""")

c.execute("""CREATE TABLE IF NOT EXISTS Author (
            authorID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
)""")

c.execute("""CREATE TABLE IF NOT EXISTS orders (
            orderID TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            totalAmt FLOAT NOT NULL,
            date DATETIME NOT NULL
          )""")

c.execute("""CREATE TABLE IF NOT EXISTS orderItem (
            orderID TEXT NOT NULL,
            ISBN TEXT NOT NULL,
            quantity INT NOT NULL,
            unitPrice FLOAT NOT NULL,
            PRIMARY KEY(orderID, ISBN),
            FOREIGN KEY(ISBN) REFERENCES bookData(ISBN),
            FOREIGN KEY(orderID) REFERENCES orders(orderID) ON DELETE CASCADE
          )""")

c.execute("""CREATE TABLE IF NOT EXISTS Review (
            username TEXT NOT NULL,
            ISBN TEXT NOT NULL,
            date DATETIME NOT NULL,
            score INT NOT NULL,
            comment TEXT,
            usefulness INT DEFAULT 0,
            PRIMARY KEY(username, ISBN),
            FOREIGN KEY(ISBN) REFERENCES bookData(ISBN),
            FOREIGN KEY(username) REFERENCES Customer(username)
          )""")

c.execute("""CREATE TABLE IF NOT EXISTS Trust (
            fromUsername TEXT NOT NULL,
            toUsername TEXT NOT NULL,
            trustScore INT NOT NULL,
            PRIMARY KEY(fromUsername, toUsername)
          )""")
c.execute("""CREATE TABLE IF NOT EXISTS Usefulness (
            fromUsername TEXT NOT NULL,
            toUsername TEXT NOT NULL,
            ISBN TEXT NOT NULL,
            PRIMARY KEY(fromUsername, toUsername, ISBN)
          )""")

c.execute("""CREATE TABLE IF NOT EXISTS requestedBook (
            username TEXT NOT NULL,
            ISBN TEXT NOT NULL,
            name TEXT,
            language TEXT,
            publisher text,
            PRIMARY KEY(username, ISBN),
            FOREIGN KEY(username) REFERENCES Customer(username)
)
""")
c.execute("""CREATE TABLE IF NOT EXISTS requestedCredit (
            date DATETIME NOT NULL,
            username TEXT PRIMARY KEY,
            amount TEXT NOT NULL,
            FOREIGN KEY(username) REFERENCES Customer(username)
)
""")

c.execute("""CREATE TABLE IF NOT EXISTS containKeyword (
            ISBN TEXT NOT NULL,
            keywordID INT NOT NULL
)""")


c.execute("""CREATE TABLE IF NOT EXISTS Keyword (
            keywordID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
)""")

c.execute("""CREATE TABLE IF NOT EXISTS rentals (
            orderID TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            totalAmt FLOAT NOT NULL,
            date DATETIME NOT NULL,
            FOREIGN KEY(orderID) REFERENCES orderItem(orderID)
          )""")

c.execute("""CREATE TABLE IF NOT EXISTS rentalItem (
            orderID TEXT NOT NULL,
            ISBN TEXT NOT NULL,
            quantity INT NOT NULL,
            unitPrice FLOAT NOT NULL,
            PRIMARY KEY(orderID, ISBN),
            FOREIGN KEY(ISBN) REFERENCES bookData(ISBN),
            FOREIGN KEY(orderID) REFERENCES orders(orderID) ON DELETE CASCADE
          )""")

# c.execute("""CREATE TABLE IF NOT EXISTS Order(
#             username TEXT,
#             ISBN TEXT,
#             quantity INT,
#             orderID INT,
#             PRIMARY KEY(orderID, username),
#             FOREIGN KEY(username) REFERENCES Customer(username),
#             FOREIGN KEY(ISBN) REFERENCES bookData(ISBN));""")

# c.execute(
#     'INSERT INTO Manager(username, password, firstName, lastName, phone, address) VALUES (?, ?, ?, ?, ?, ?)', ('manager1', 'password', 'firstName', 'lastName', 81444417393, 'address'))

# c.execute("""INSERT INTO `Customer` (`id`, `username`, `password`, `email`) VALUES(1, 'test', 'test', 'test@test.com')""")
# c.execute("""SELECT * FROM Customer""")
# # c.execute("""DROP TABLE Customer""")
# data = c.fetchall()
# for d in data:
#     print(d)
# c.execute("""DELETE FROM bookData WHERE ISBN = 'ISBN123456789'""")
# c.execute("""INSERT INTO bookData VALUES('ISBN123456789', 'The Untold Story', 'English','The House', '2002-03-25', 50, 25, 'Life', 200)""")
# conn.commit()
# c.execute("""INSERT INTO bookData VALUES('ISBN000000000', 'The Told Story', 'English','BNPS', '2010-06-23', 60, 30, 'Not Life', 2500)""")
# conn.commit()
# c.execute("""SELECT * FROM Manager""")
# # c.execute('INSERT INTO Keyword(name) VALUES ("HELLO")')
conn.commit()
# c.execute("SELECT keywordID FROM Keyword where name='HELLO'")
# data = c.fetchone()
# print(data[0])
# for d in data:
#     print(d)
