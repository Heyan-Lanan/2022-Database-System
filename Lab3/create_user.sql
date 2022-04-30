drop table if exists User;
create table User
(
    User_Name varchar(50) not null,
    User_Password varchar(50) not null,
    primary key (User_Name)
);