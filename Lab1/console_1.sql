select	Book.name, borrow.Borrow_date
from	Book, Reader, Borrow
where	Reader.ID=Borrow.Reader_ID
    and Borrow.book_ID=Book.ID
    and Reader.name='Rose';
