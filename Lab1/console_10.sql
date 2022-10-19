select	reader.ID, reader.name, reader.age, count(book_ID) as sum
from	Reader, Book, Borrow
where   Reader.ID = Borrow.Reader_ID
    and book.ID = borrow.book_ID
    and borrow.Borrow_Date > '2021-1-1 00:00:00'
    and borrow.Borrow_Date < '2022-1-1 00:00:00'
group by reader.ID
order by (sum) desc
limit 0, 20