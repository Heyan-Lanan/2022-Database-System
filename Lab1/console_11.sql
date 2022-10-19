set @old_book_id = 'b1';
set @new_book_id = 'b100000';
call re_define_book_id(
        @old_book_id,
        @new_book_id
    );