-- SQLite
SELECT ISBN, sum(quantity) FROM orderItem GROUP BY ISBN

-- SQLite
-- used for functionality 13(b)
SELECT A.ISBN, Author.name, A.qty FROM (SELECT ISBN, sum(quantity) AS qty FROM orderItem GROUP BY ISBN) AS A INNER JOIN writtenBy ON A.ISBN=writtenBy.ISBN INNER JOIN Author on Author.authorID=writtenBy.authorID ORDER BY A.qty DESC
-- SQLite
SELECT A.ISBN, A.qty, bookData.publisher FROM (SELECT ISBN, sum(quantity) AS qty FROM orderItem GROUP BY ISBN) AS A INNER JOIN bookData ON A.ISBN = bookData.ISBN ORDER BY A.qty DESC


-- SQLite
UPDATE Review SET usefulness = 0 WHERE username = "abcd"

--SQLite
SELECT * FROM Customer ORDER BY trustCount DESC LIMIT 1

--SQLite
ALTER TABLE Usefulness ADD value INT  DEFAULT 1

--SQLite
DELETE FROM Usefulness WHERE fromUsername = "abcd";

--SQLite BookStatistics by quantity 
SELECT orderItem.ISBN, name, SUM(quantity) AS qty FROM orderItem INNER JOIN bookData on orderItem.ISBN = bookData.ISBN GROUP BY orderItem.ISBN ORDER BY qty DESC LIMIT 1;

--SQLite
SELECT Author.name, A.qty FROM (SELECT ISBN, sum(quantity) AS qty FROM orderItem GROUP BY ISBN) AS A INNER JOIN writtenBy ON A.ISBN=writtenBy.ISBN INNER JOIN Author on Author.authorID=writtenBy.authorID ORDER BY A.qty DESC LIMIT 2

--SQLite
DELETE FROM writtenBy

--SQLite
SELECT bookData.*, Author.name,AVG(score) FROM bookData LEFT JOIN writtenBy on Author ON bookData.authorID = Author.authorID LEFT JOIN Review ON bookData.ISBN = Review.ISBN GROUP BY Review.ISBN ORDER BY ?

--SQLite

SELECT bookData.*, writtenBy.authorID FROM bookData LEFT JOIN writtenBy on bookData.ISBN = writtenBy.ISBN 

--SQLite ALL BOOKS WITH THEIR AUTHOR NAMES
SELECT Author.authorID, name, ISBN FROM writtenBy LEFT JOIN Author ON writtenBy.authorID=Author.authorID
SELECT bookData.*, A.name AS author FROM bookData LEFT JOIN (SELECT Author.authorID, name, ISBN FROM writtenBy LEFT JOIN Author ON writtenBy.authorID=Author.authorID) AS A ON bookData.ISBN=A.ISBN

SELECT bookData.*, AVG(score) FROM bookData LEFT JOIN (SELECT Author.authorID, name, ISBN FROM writtenBy LEFT JOIN Author ON writtenBy.authorID=Author.authorID) AS A ON bookData.ISBN=A.ISBN LEFT JOIN Review ON bookData.ISBN = Review.ISBN GROUP BY bookData.ISBN 


SELECT bookData.* FROM bookData LEFT JOIN (SELECT Author.authorID, name, ISBN FROM writtenBy LEFT JOIN Author ON writtenBy.authorID=Author.authorID) AS A ON bookData.ISBN=A.ISBN LEFT JOIN Review ON bookData.ISBN = Review.ISBN GROUP BY bookData.ISBN 


SELECT * FROM Review where username IN (SELECT username FROM Customer WHERE trustCount>0)

SELECT bookData.*, AVG(score) FROM bookData LEFT JOIN (SELECT Author.authorID, name, ISBN FROM writtenBy LEFT JOIN Author ON writtenBy.authorID=Author.authorID) AS A ON bookData.ISBN=A.ISBN LEFT JOIN (SELECT * FROM Review where username IN (SELECT username FROM Customer WHERE trustCount>0)) AS R ON bookData.ISBN = R.ISBN GROUP BY bookData.ISBN 

--Books a user own
SELECT ISBN from orders LEFT JOIN orderItem on orders.orderID = orderItem.orderID where username = "victor"

--Order ID of orders with that books in other orders
SELECT orderID FROM orderItem  WHERE ISBN in (SELECT ISBN from orders LEFT JOIN orderItem on orders.orderID = orderItem.orderID where username = "victor") 
--GET THE USERNAME from this: username of people who own the same book
SELECT DISTINCT(username) FROM orderItem LEFT JOIN orders ON orderItem.orderID=orders.orderID  WHERE ISBN in (SELECT ISBN from orders LEFT JOIN orderItem on orders.orderID = orderItem.orderID where username = "victor") 
--Books that the above users own
SELECT DISTINCT(ISBN) FROM orders LEFT JOIN orderItem on orders.orderID = orderItem.orderID WHERE username IN (SELECT DISTINCT(username) FROM orderItem LEFT JOIN orders ON orderItem.orderID=orders.orderID  WHERE ISBN in (SELECT ISBN from orders LEFT JOIN orderItem on orders.orderID = orderItem.orderID where username = "victor") )
--REMOVING THE BOOK USER ALREADY HAVE
SELECT ISBN FROM (SELECT DISTINCT(ISBN) FROM orders LEFT JOIN orderItem on orders.orderID = orderItem.orderID WHERE username IN (SELECT DISTINCT(username) FROM orderItem LEFT JOIN orders ON orderItem.orderID=orders.orderID  WHERE ISBN in (SELECT ISBN from orders LEFT JOIN orderItem on orders.orderID = orderItem.orderID where username = "victor"))) AS A WHERE A.ISBN NOT IN (SELECT ISBN from orders LEFT JOIN orderItem on orders.orderID = orderItem.orderID where username = "victor")
SELECT * FROM bookData WHERE ISBN IN (SELECT ISBN FROM (SELECT DISTINCT(ISBN) FROM orders LEFT JOIN orderItem on orders.orderID = orderItem.orderID WHERE username IN (SELECT DISTINCT(username) FROM orderItem LEFT JOIN orders ON orderItem.orderID=orders.orderID  WHERE ISBN in (SELECT ISBN from orders LEFT JOIN orderItem on orders.orderID = orderItem.orderID where username = "victor"))) AS A WHERE A.ISBN NOT IN (SELECT ISBN from orders LEFT JOIN orderItem on orders.orderID = orderItem.orderID where username = "victor"))
--ISBN OF  books in other orders
SELECT ISBN FROM orderItem WHERE orderID IN (SELECT orderID from orderItem  WHERE ISBN in (SELECT ISBN from orders LEFT JOIN orderItem on orders.orderID = orderItem.orderID where username = "victor") )

--CHANGING BEFORE THIS
--Books to suggest
SELECT DISTINCT(ISBN) FROM (SELECT orderID from orderItem  WHERE ISBN in (SELECT ISBN from orders LEFT JOIN orderItem on orders.orderID = orderItem.orderID where username = "victor")) AS A LEFT JOIN orderItem ON A.orderID = orderItem.orderID 

--BOOKS ISBN TO SUGGEST ALREADY NOT IN ORDER
SELECT DISTINCT(ISBN) FROM (SELECT orderID from orderItem  WHERE ISBN in (SELECT ISBN from orders LEFT JOIN orderItem on orders.orderID = orderItem.orderID where username = "victor")) AS A LEFT JOIN orderItem ON A.orderID = orderItem.orderID WHERE ISBN NOT IN (SELECT ISBN from orders LEFT JOIN orderItem on orders.orderID = orderItem.orderID where username = "victor")

-- display all data of book suggestion
SELECT * FROM bookData WHERE ISBN IN (SELECT DISTINCT(ISBN) FROM (SELECT orderID from orderItem  WHERE ISBN in (SELECT ISBN from orders LEFT JOIN orderItem on orders.orderID = orderItem.orderID where username = "victor")) AS A LEFT JOIN orderItem ON A.orderID = orderItem.orderID WHERE ISBN NOT IN (SELECT ISBN from orders LEFT JOIN orderItem on orders.orderID = orderItem.orderID where username = "victor"))



--get authorID of X
SELECT authorID FROM Author WHERE name = "Keshav"
--Books written by X
SELECT ISBN, authorID FROM writtenBy WHERE authorID = (SELECT authorID FROM Author WHERE name = "Keshav")
--cross with table with all information book and authorID--: first Degree
-- SELECT authorID FROM writtenBy, (SELECT ISBN, authorID FROM writtenBy WHERE authorID = (SELECT authorID FROM Author WHERE name = "Keshav")
-- ) AS 
--isbn of books with count>2 in writtenby
SELECT ISBN count(ISBN) FROM writtenBy GROUP BY ISBN 
--cross book with condition: 

--Select ISBN of book written by X in count>2 table
SELECT ISBN FROM (SELECT ISBN FROM writtenBy WHERE authorID = (SELECT authorID FROM Author WHERE name = "Keshav")) AS A WHERE A.ISBN IN (SELECT ISBN FROM writtenBy GROUP BY ISBN )

--Now look for authors of this ISBN
SELECT ISBN, writtenBy.authorID, name AS authorName FROM writtenBy LEFT JOIN Author ON writtenBy.authorID = Author.authorID WHERE ISBN IN (SELECT ISBN FROM (SELECT ISBN FROM writtenBy WHERE authorID = (SELECT authorID FROM Author WHERE name = "Keshav")) AS A WHERE A.ISBN IN (SELECT ISBN FROM writtenBy GROUP BY ISBN ))

--NOW REMOVING THE AuthorName we started with : 1 Degree separated
SELECT * FROM (SELECT ISBN, writtenBy.authorID, name AS authorName FROM writtenBy LEFT JOIN Author ON writtenBy.authorID = Author.authorID WHERE ISBN IN (SELECT ISBN FROM (SELECT ISBN FROM writtenBy WHERE authorID = (SELECT authorID FROM Author WHERE name = "Keshav")) AS A WHERE A.ISBN IN (SELECT ISBN FROM writtenBy GROUP BY ISBN ))) WHERE authorName != "Keshav"

--To display correctly on front end instaead of * print authorID and author name only

--to update manager password
UPDATE Manager SET password="$2b$12$AjDqOYjvfe/b4hS/lI2TqurCMNBevmHrE0rp4aaRhVKARIWfVbx5O"

update Customer SET balance = -10 WHERE username="victor"
--Correcting Data
DELETE FROM Review WHERE score = 5 
DELETE FROM Trust

--Two degree
SELECT authorID, ISBN FROM (SELECT ISBN, writtenBy.authorID, name AS authorName FROM writtenBy LEFT JOIN Author ON writtenBy.authorID = Author.authorID WHERE ISBN IN (SELECT ISBN FROM (SELECT ISBN FROM writtenBy WHERE authorID = (SELECT authorID FROM Author WHERE name = "Keshav")) AS A WHERE A.ISBN IN (SELECT ISBN FROM writtenBy GROUP BY ISBN ))) WHERE authorName != "Keshav"
--big table saare authorid saare isbn cross with ^ condition: isbn same authorID not X




--all authorID and isbn:
SELECT A.authorID, A.ISBN FROM (SELECT authorID, ISBN FROM (SELECT ISBN, writtenBy.authorID, name AS authorName FROM writtenBy LEFT JOIN Author ON writtenBy.authorID = Author.authorID WHERE ISBN IN (SELECT ISBN FROM (SELECT ISBN FROM writtenBy WHERE authorID = (SELECT authorID FROM Author WHERE name = "Keshav")) AS A WHERE A.ISBN IN (SELECT ISBN FROM writtenBy GROUP BY ISBN ))) WHERE authorName != "Keshav") AS A, writtenBy WHERE A.ISBN = writtenBy.ISBN


UPDATE Customer SET balance = 0 WHERE username = "victor"


--ONE DEGREE SEPARATION
SELECT authorID, authorName FROM (SELECT ISBN, writtenBy.authorID, name AS authorName FROM writtenBy LEFT JOIN Author ON writtenBy.authorID = Author.authorID WHERE ISBN IN (SELECT ISBN FROM (SELECT ISBN FROM writtenBy WHERE authorID =8) AS A WHERE A.ISBN IN (SELECT ISBN FROM writtenBy GROUP BY ISBN ))) WHERE authorID != 8

--One degree book detail
SELECT * FROM bookData WHERE ISBN IN (SELECT ISBN FROM writtenBy WHERE authorID IN (SELECT authorID FROM (SELECT ISBN, writtenBy.authorID, name AS authorName FROM writtenBy LEFT JOIN Author ON writtenBy.authorID = Author.authorID WHERE ISBN IN (SELECT ISBN FROM (SELECT ISBN FROM writtenBy WHERE authorID =8) AS A WHERE A.ISBN IN (SELECT ISBN FROM writtenBy GROUP BY ISBN ))) WHERE authorID != 8))

--TWO DEGREE SEPARATION
SELECT C.authorID FROM writtenBy AS C, writtenBy AS D WHERE D.authorID IN (SELECT authorID FROM (SELECT ISBN, writtenBy.authorID, name AS authorName FROM writtenBy LEFT JOIN Author ON writtenBy.authorID = Author.authorID WHERE ISBN IN (SELECT ISBN FROM (SELECT ISBN FROM writtenBy WHERE authorID =7) AS A WHERE A.ISBN IN (SELECT ISBN FROM writtenBy GROUP BY ISBN ))) WHERE authorID != 7) AND C.authorID NOT IN ((SELECT authorID FROM (SELECT ISBN, writtenBy.authorID, name AS authorName FROM writtenBy LEFT JOIN Author ON writtenBy.authorID = Author.authorID WHERE ISBN IN (SELECT ISBN FROM (SELECT ISBN FROM writtenBy WHERE authorID =7) AS A WHERE A.ISBN IN (SELECT ISBN FROM writtenBy GROUP BY ISBN ))) WHERE authorID != 7)) AND D.ISBN = C.ISBN AND C.authorID !=7
SELECT * FROM Author WHERE authorID IN (SELECT C.authorID FROM writtenBy AS C, writtenBy AS D WHERE D.authorID IN (SELECT authorID FROM (SELECT ISBN, writtenBy.authorID, name AS authorName FROM writtenBy LEFT JOIN Author ON writtenBy.authorID = Author.authorID WHERE ISBN IN (SELECT ISBN FROM (SELECT ISBN FROM writtenBy WHERE authorID =7) AS A WHERE A.ISBN IN (SELECT ISBN FROM writtenBy GROUP BY ISBN ))) WHERE authorID != 7) AND C.authorID NOT IN ((SELECT authorID FROM (SELECT ISBN, writtenBy.authorID, name AS authorName FROM writtenBy LEFT JOIN Author ON writtenBy.authorID = Author.authorID WHERE ISBN IN (SELECT ISBN FROM (SELECT ISBN FROM writtenBy WHERE authorID =7) AS A WHERE A.ISBN IN (SELECT ISBN FROM writtenBy GROUP BY ISBN ))) WHERE authorID != 7)) AND D.ISBN = C.ISBN AND C.authorID !=7)
--Select book in two degree
SELECT * FROM bookData WHERE ISBN IN (SELECT ISBN FROM writtenBy WHERE authorID IN (SELECT C.authorID FROM writtenBy AS C, writtenBy AS D WHERE D.authorID IN (SELECT authorID FROM (SELECT ISBN, writtenBy.authorID, name AS authorName FROM writtenBy LEFT JOIN Author ON writtenBy.authorID = Author.authorID WHERE ISBN IN (SELECT ISBN FROM (SELECT ISBN FROM writtenBy WHERE authorID =8) AS A WHERE A.ISBN IN (SELECT ISBN FROM writtenBy GROUP BY ISBN ))) WHERE authorID != 8) AND C.authorID NOT IN ((SELECT authorID FROM (SELECT ISBN, writtenBy.authorID, name AS authorName FROM writtenBy LEFT JOIN Author ON writtenBy.authorID = Author.authorID WHERE ISBN IN (SELECT ISBN FROM (SELECT ISBN FROM writtenBy WHERE authorID =8) AS A WHERE A.ISBN IN (SELECT ISBN FROM writtenBy GROUP BY ISBN ))) WHERE authorID != 8)) AND D.ISBN = C.ISBN AND C.authorID !=8) )


DELETE FROM bookData
DELETE FROM writtenBy

SELECT ISBN FROM writtenBy WHERE authorID IN (SELECT authorID FROM (SELECT ISBN, writtenBy.authorID, name AS authorName FROM writtenBy LEFT JOIN Author ON writtenBy.authorID = Author.authorID WHERE ISBN IN (SELECT ISBN FROM (SELECT ISBN FROM writtenBy WHERE authorID =8) AS A WHERE A.ISBN IN (SELECT ISBN FROM writtenBy GROUP BY ISBN ))) WHERE authorID != 8)

DELETE FROM orders WHERE orderID = "233b8b64a9e311ebbab5a683e7850434"
DELETE FROM orderItem


SELECT bookData.*, AVG(score), A.name AS author FROM bookData LEFT JOIN (SELECT Author.authorID, name, ISBN FROM writtenBy LEFT JOIN Author ON writtenBy.authorID=Author.authorID) AS A ON bookData.ISBN=A.ISBN LEFT JOIN (SELECT * FROM Review where username IN (SELECT username FROM Customer WHERE trustCount>0)) AS R ON bookData.ISBN = R.ISBN WHERE bookData.name like "%" AND publisher like "%" AND language like "%" AND author like "%" GROUP BY bookData.ISBN ORDER BY AVG(score)

--All book (repititive) with their all authorname and keywords
SELECT bookData.ISBN, bookData.name, language, publisher, date, stock, price, subject, noOfPages, Author.authorID, Author.name as authorName, Keyword.keywordID, Keyword.name as keywordName FROM bookData JOIN writtenBy on bookData.ISBN = writtenBy.ISBN JOIN Author ON writtenBy.authorID = Author.authorID JOIN containKeyword ON bookData.ISBN = containKeyword.ISBN JOIN Keyword ON containKeyword.keywordID = Keyword.keywordID

--Now searching on query given by user
SELECT * FROM (SELECT bookData.ISBN, bookData.name, language, publisher, date, stock, price, subject, noOfPages, Author.authorID, Author.name as authorName, Keyword.keywordID, Keyword.name as keywordName FROM bookData JOIN writtenBy on bookData.ISBN = writtenBy.ISBN JOIN Author ON writtenBy.authorID = Author.authorID JOIN containKeyword ON bookData.ISBN = containKeyword.ISBN JOIN Keyword ON containKeyword.keywordID = Keyword.keywordID) WHERE name like "%" AND publisher like "%" AND language like "%" AND authorName like "%" AND keywordName like "%" GROUP BY ISBN

--ADDING AVG SCORE
SELECT A.*, avg(score) FROM (SELECT * FROM (SELECT bookData.ISBN, bookData.name, language, publisher, date, stock, price, subject, noOfPages, Author.authorID, Author.name as authorName, Keyword.keywordID, Keyword.name as keywordName FROM bookData JOIN writtenBy on bookData.ISBN = writtenBy.ISBN JOIN Author ON writtenBy.authorID = Author.authorID JOIN containKeyword ON bookData.ISBN = containKeyword.ISBN JOIN Keyword ON containKeyword.keywordID = Keyword.keywordID) WHERE name like "%" AND publisher like "%" AND language like "%" AND authorName like "%" AND keywordName like "%" GROUP BY ISBN) AS A JOIN Review ON A.ISBN=Review.ISBN GROUP BY A.ISBN ORDER BY AVG(score)

--AVG SCORE BY TRUSTED
SELECT A.*, avg(score) FROM (SELECT * FROM (SELECT bookData.ISBN, bookData.name, language, publisher, date, stock, price, subject, noOfPages, Author.authorID, Author.name as authorName, Keyword.keywordID, Keyword.name as keywordName FROM bookData JOIN writtenBy on bookData.ISBN = writtenBy.ISBN JOIN Author ON writtenBy.authorID = Author.authorID JOIN containKeyword ON bookData.ISBN = containKeyword.ISBN JOIN Keyword ON containKeyword.keywordID = Keyword.keywordID) WHERE name like "%" AND publisher like "%" AND language like "%" AND authorName like "%" AND keywordName like "%" GROUP BY ISBN) AS A JOIN (SELECT * FROM Review WHERE username IN (SELECT username FROM Customer WHERE trustCount>0)) AS Review ON A.ISBN=Review.ISBN GROUP BY A.ISBN ORDER BY AVG(score)

-- SEARCH BY DATE
SELECT * FROM (SELECT bookData.ISBN, bookData.name, language, publisher, date, stock, price, subject, noOfPages, Author.authorID, Author.name as authorName, Keyword.keywordID, Keyword.name as keywordName FROM bookData JOIN writtenBy on bookData.ISBN = writtenBy.ISBN JOIN Author ON writtenBy.authorID = Author.authorID JOIN containKeyword ON bookData.ISBN = containKeyword.ISBN JOIN Keyword ON containKeyword.keywordID = Keyword.keywordID) WHERE name like "%" AND publisher like "%" AND language like "%" AND authorName like "%" AND keywordName like "%" GROUP BY ISBN ORDER BY date
--Sort by date with AVG SCORE
SELECT A.*, avg(score) FROM (SELECT * FROM (SELECT bookData.ISBN, bookData.name, language, publisher, date, stock, price, subject, noOfPages, Author.authorID, Author.name as authorName, Keyword.keywordID, Keyword.name as keywordName FROM bookData JOIN writtenBy on bookData.ISBN = writtenBy.ISBN JOIN Author ON writtenBy.authorID = Author.authorID JOIN containKeyword ON bookData.ISBN = containKeyword.ISBN JOIN Keyword ON containKeyword.keywordID = Keyword.keywordID) WHERE name like "%" AND publisher like "%" AND language like "%" AND authorName like "%" AND keywordName like "%" GROUP BY ISBN) AS A JOIN Review ON A.ISBN=Review.ISBN GROUP BY A.ISBN ORDER BY date


SELECT bookData.*, Author.name, AVG(score) FROM bookData LEFT JOIN (SELECT Author.authorID, name, ISBN FROM writtenBy LEFT JOIN Author ON writtenBy.authorID=Author.authorID) AS A ON bookData.ISBN=A.ISBN LEFT JOIN Review ON bookData.ISBN = Review.ISBN GROUP BY bookData.ISBN  ORDER BY bookData.date