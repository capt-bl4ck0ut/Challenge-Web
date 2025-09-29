GRANT FILE ON *.* to 'user'@'%';
FLUSH PRIVILEGES;

USE colorfulmemo;

CREATE TABLE memo (
    id int primary key auto_increment,
    title varchar(255) not null,
    color varchar(255) not null,
    content varchar(1023) not null,
    adminCheck int not null
);
