create database project;
use project;

create table signup(
fullname char(30) not null,
email varchar(40) primary key,
username char(30) not null,
password varchar(30) not null
);

desc signup;

select * from signup;

create table contact1(
firstname varchar(50) not null,
lastname varchar(50) not null,
email varchar(50) not null,
mobile varchar(20) not null,
note varchar(1000) not null
);
desc contact;
select * from contact1;

desc contact1;

alter table contact modify mobile varchar(20);
drop table contact;
