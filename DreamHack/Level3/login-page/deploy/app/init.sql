CREATE DATABASE reset_db CHARACTER SET utf8;
CREATE USER 'dbuser'@'localhost' IDENTIFIED BY 'dbpass';
GRANT ALL PRIVILEGES ON reset_db.* TO 'dbuser'@'localhost';

USE `reset_db`;
CREATE TABLE users (
  idx int auto_increment primary key,
  username varchar(128) not null,
  password varchar(128) not null
);

INSERT INTO users (username, password) values ('admin', 'initial_passwordqwer1234');
