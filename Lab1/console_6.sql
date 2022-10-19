select name, ID
from Reader
where NOT EXISTS(
    select *
    from Borrow
    where Reader.ID = Borrow.Reader_ID
        and book_ID in (
            select Book_ID
            from Reader, Borrow
            where Reader.ID = Borrow.Reader_ID
                and Reader.name = '李林'
        )
    );