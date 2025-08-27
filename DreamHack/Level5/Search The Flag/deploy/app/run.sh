#!/bin/sh

export MYSQL_USER=search_user
export MYSQL_PASSWORD=search_password

/usr/bin/mysqld_safe &
sleep 4
python3 app.py
