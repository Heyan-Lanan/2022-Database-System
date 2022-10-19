DROP view IF EXISTS Message;
create view Message as(
    select	borrow.Reader_ID, Reader.name as Reader_name, borrow.Book_ID, Book.name as Book_name, Borrow.Borrow_date
	from	Reader, Book, Borrow
	where	Reader.ID = Borrow.Reader_ID
	    and Borrow.book_ID = Book.ID
	);