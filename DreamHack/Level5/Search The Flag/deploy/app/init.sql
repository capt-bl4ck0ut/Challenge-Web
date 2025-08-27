CREATE DATABASE search_db CHARACTER SET utf8;
CREATE USER 'search_user'@'localhost' IDENTIFIED BY 'search_password';
GRANT ALL PRIVILEGES ON search_db.* TO 'search_user'@'localhost';

USE `search_db`;
DROP TABLE IF EXISTS `users`;
CREATE TABLE users (
  idx int auto_increment primary key,
  username varchar(128) not null,
  password varchar(128) not null
);

DROP TABLE IF EXISTS `sentences`;
CREATE TABLE sentences (
  idx int auto_increment primary key,
  sentence varchar(256) not null,
  secret TINYINT(1) not null
);


INSERT INTO users (username, password) values ('admin', '99a79f8c93d70c2aea82868e4e70f04ec2cec64edbf6885ca0e0ab0c7f910150');

INSERT INTO sentences (sentence, secret) VALUES
  ('The harder the battle, the sweeter the victory.', 0),
  ('In football, the worst blindness is only seeing the ball.', 0),
  ("Success is no accident. It is hard work, perseverance, learning, studying, sacrifice, and most of all, love of what you are doing.", 0),
  ("If you're not making mistakes, then you're not doing anything. I'm positive that a doer makes mistakes.", 0),
  ("I don't have time for fear. I'm too busy working on my dreams.", 0),
  ('The only way to do great work is to love what you do.', 0),
  ('The best way to predict the future is to create it.', 0),
  ("Your time is limited, don't waste it living someone else's life.", 0),
  ("The only limit to our realization of tomorrow will be our doubts of today.", 0),
  ("DH{**fake_flag**}", 1);