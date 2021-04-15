import sqlite3

conn = sqlite3.connect('Book.db')

c = conn.cursor()

# c.execute("""CREATE TABLE IF NOT EXISTS `Customer` (
# 	`id` int(11) NOT NULL,
#   	`username` varchar(50) NOT NULL,
#   	`password` varchar(255) NOT NULL,
#   	`email` varchar(100) NOT NULL,
#     PRIMARY KEY (`id`)
# )""")
c.execute("""CREATE TABLE IF NOT EXISTS Customer (
            username TEXT PRIMARY KEY,
            password TEXT,
            firstName TEXT,
            lastName TEXT,
            phone INT,
            address TEXT,
            balance FLOAT DEFAULT 0,
            dateOfJoining DATETIME DEFAULT CURRENT_TIMESTAMP)""")


# c.execute("""INSERT INTO `Customer` (`id`, `username`, `password`, `email`) VALUES (1, 'test', 'test', 'test@test.com')""")
c.execute("""SELECT * FROM Customer""")
# c.execute("""DROP TABLE Customer""")
data = c.fetchall()
for d in data:
    print(d)
