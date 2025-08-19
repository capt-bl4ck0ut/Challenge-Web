from pymysql import connect, cursors

class manager:
    def __init__(self):
        self.connect()

    def connect(self):
        self.conn = connect(host = "database", user = "feeling", passwd = "8cb6315a2961316c79be9f96a31e62d6", db = "members", cursorclass = cursors.DictCursor)

    def cursor(self):
        self.cursor = self.conn.cursor()

    def execute(self, query):
        try:
            self.cursor.execute(query)
        except BaseException:
            pass

    def fetch_all(self):
        try: 
            return self.cursor.fetchall()
        except BaseException:
            pass

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
