select	name
from	Reader
where	ID IN(
    select Reader.ID
	from  Reader,Borrow
	where	Reader.ID = Borrow.Reader_ID
    group by	Reader.ID
    having	count(book_ID)>3
    );