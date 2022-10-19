Create table Book
(
    ID     char(8) Primary Key,
    name   varchar(50) NOT NULL,
    author varchar(10),
    price  float,
    status int Default 0
);
Create table Reader
(
    ID      char(8) Primary Key,
    name    varchar(10),
    age     int,
    address varchar(20)
);
Create table Borrow
(
    book_ID     char(8),
    Reader_ID   char(8),
    Borrow_Data date,
    Return_Data date,
    Primary Key (book_ID, Reader_ID),
    Foreign Key (book_ID) references Book (ID),
    Foreign Key (Reader_ID) references Reader (ID)
);
