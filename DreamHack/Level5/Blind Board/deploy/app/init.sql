CREATE DATABASE blind_board_db CHARACTER SET utf8;
CREATE USER 'dbuser'@'localhost' IDENTIFIED BY 'dbpass';
GRANT ALL PRIVILEGES ON blind_board_db.* TO 'dbuser'@'localhost';

USE `blind_board_db`;
-- users table creation
CREATE TABLE users (
  idx int auto_increment primary key,
  uid varchar(128) not null,
  upw varchar(128) not null
);

INSERT INTO users (uid, upw) values ('admin', 'DH{**flag**}');
INSERT INTO users (uid, upw) values ('guest', 'guest');
INSERT INTO users (uid, upw) values ('test', 'test');

-- articles table creation
CREATE TABLE articles (
  idx int auto_increment primary key,
  title varchar(96) not null,
  content varchar(4096) not null
);

INSERT INTO articles (title, content) values ('First article :)', 'Is this board secure?');
INSERT INTO articles (title, content) values ('zxcvxzcvxcvxcvxcvxcvxcv', 'zxcvjzxcvxvlxkcvqwerqwerlqwkerhwqelrqher');
INSERT INTO articles (title, content) values ('hehehehehehehe', 'heheheheehehehehehehehohohhohohohohahahahahahahahahaha');
INSERT INTO articles (title, content) values ('hehehehehehehe', 'heheheheehehehehehehehohohhohohohohahahahahahahahahaha');
INSERT INTO articles (title, content) values ('hehehehehehehe', 'heheheheehehehehehehehohohhohohohohahahahahahahahahaha');
INSERT INTO articles (title, content) values ('한글도 되는 게시판인가?', 'ㅁㄴㅇㄹㅁㄴㅇㄹ');

FLUSH PRIVILEGES;
