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

