-- SQLite
SELECT bookData.*, AVG(score) FROM bookData, Review WHERE bookData.ISBN = Review.ISBN GROUP BY Review.ISBN;

-- SQLite
SELECT bookData.*, Author.name AS Author Name ,AVG(score) FROM bookData LEFT JOIN Author ON bookData.authorID = Author.authorID LEFT JOIN Review ON bookData.ISBN = Review.ISBN GROUP BY Review.ISBN