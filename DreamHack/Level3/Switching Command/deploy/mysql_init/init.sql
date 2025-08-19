SET NAMES utf8;

DROP TABLE IF EXISTS `users`;
CREATE TABLE users (
  idx int auto_increment primary key,
  username varchar(30) not null,
  password varchar(100) not null
);
INSERT INTO users (username, password) values ('admin', '***REDACTED***');