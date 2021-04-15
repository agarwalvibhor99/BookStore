import sqlite3

conn = sqlite3.connect('Book.db')

c = conn.cursor()


c.execute("""CREATE TABLE IF NOT EXISTS Customer (
            username TEXT PRIMARY KEY,
            password TEXT,
            firstName TEXT,
            lastName TEXT,
            phone INT,
            address TEXT,
            balance FLOAT DEFAULT 0,
            dateOfJoining DATETIME DEFAULT CURRENT_TIMESTAMP)""")

c.execute("""CREATE TABLE IF NOT EXISTS Manager (
            username TEXT PRIMARY KEY,
            password TEXT,
            firstName TEXT,
            lastName TEXT,
            phone INT,
            address TEXT,
            salary FLOAT DEFAULT 0,
            booksAdded INT DEFAULT 0)""")

c.execute("""CREATE TABLE IF NOT EXISTS bookData (
            ISBN TEXT PRIMARY KEY,
            name TEXT,
            authorID INT,
            publisher text,
            date DATETIME,
            stock INT,
            price float,
            subject TEXT,
            noOfPages INT
            )""")
c.execute("""CREATE TABLE IF NOT EXISTS writtenBy (
            ISBN TEXT,
            authorID INT,
            PRIMARY KEY(ISBN, authorID),
            FOREIGN KEY(ISBN) REFERENCES bookData(ISBN),
            FOREIGN KEY(authorID) REFERENCES bookData(authorID)
)""")
c.execute("""CREATE TABLE IF NOT EXISTS Author (
            authorID INT PRIMARY KEY,
            name TEXT
)""")

# c.execute(
#     'INSERT INTO Manager(username, password, firstName, lastName, phone, address) VALUES (?, ?, ?, ?, ?, ?)', ('manager1', 'password', 'firstName', 'lastName', 81444417393, 'address'))

# c.execute("""INSERT INTO `Customer` (`id`, `username`, `password`, `email`) VALUES(1, 'test', 'test', 'test@test.com')""")
# c.execute("""SELECT * FROM Customer""")
# # c.execute("""DROP TABLE Customer""")
# data = c.fetchall()
# for d in data:
#     print(d)
c.execute("""SELECT * FROM Manager""")

data = c.fetchall()
for d in data:
    print(d)
