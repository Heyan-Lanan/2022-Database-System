#select count(*)
#from t
select count(book.id)
from borrow,
     book
where borrow.book_id = book.id
  and (
                book.status <> 1
            and EXISTS(
                        select *
                        from borrow
                        where borrow.Return_Date is null
                          and borrow.book_id = book.id
                    )
        or
                book.status <> 0
                    and not EXISTS(
                        select *
                        from borrow
                        where borrow.Return_Date is null
                          and borrow.book_id = book.id
                    )
    )
group by book.id;

