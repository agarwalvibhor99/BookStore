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
SELECT A.ISBN, Author.name, A.qty FROM (SELECT authorID, sum(quantity) AS qty FROM orderItem GROUP BY authorID) AS A INNER JOIN Author ON A.authorID=Author.authorIDORDER BY A.qty DESC LIMIT 1