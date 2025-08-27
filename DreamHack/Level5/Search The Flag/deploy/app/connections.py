import pymysql
from os import environ


def connect_mysql():
    db = pymysql.connect(
        host="localhost",
        port=3306,
        user=environ["MYSQL_USER"],
        passwd=environ["MYSQL_PASSWORD"],
        db="search_db",
        charset="utf8",
    )
    cursor = db.cursor()
    return db, cursor