drop table if exists posts;
create table posts(
    id integer primary key autoincrement,
    title text not null,
    text text not null
);

insert into posts (title, text) values
('First Entry', 'This is some text');
insert into posts (title, text) values
('Second Entry', 'Here is some more text');

insert into posts (title, text) values
('Third Entry', 'And this is some more text again');