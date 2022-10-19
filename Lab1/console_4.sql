select	borrow.Book_ID, Book.name
from	Reader, Book, Borrow
where	Reader.ID = Borrow.Reader_ID
    and Borrow.book_ID = Book.ID
    and Reader.name = '李林'
    and return_date is NULL;