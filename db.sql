create database game_cards;
use game_cards;
create table user (
	id int auto_increment primary key,
    name varchar(20),
    balance int
);
insert into user (name, balance) values ("hau", 0);
insert into user (name, balance) values ("nguyen", 0);
insert into user (name, balance) values ("nam", 0);
insert into user (name, balance) values ("thien", 0);