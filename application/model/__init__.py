import sqlite3


class SqliteClient:
    def __init__(self):
        self.conn = sqlite3.connect('blacklist.db')
        self.tablename = 'blacklist'
        self.create()

    def create(self):
        cursor = self.conn.cursor()
        y = cursor.execute(f"select count(*) from sqlite_master where type ='table' and name ='{self.tablename}'")
        if y.fetchone()[0] > 0:
            return
        cursor.execute(f'create table {self.tablename}(id integer primary key autoincrement, ip varchar(20))')
        cursor.close()
        self.conn.commit()

    def query(self):
        cursor = self.conn.cursor()
        res = cursor.execute(f'select ip from {self.tablename}')
        return res.fetchall()

    def load_ip(self):
        res = self.query()
        data = set()
        for i in res:
            data.add(i[0])
        return data

    def push(self, data):
        cursor = self.conn.cursor()
        cursor.execute(f'insert into {self.tablename} (ip) values ("{data}")')
        cursor.close()
        self.conn.commit()

    def pop(self, data):
        cursor = self.conn.cursor()
        cursor.execute(f'delete from {self.tablename} where ip = "{data}"')
        cursor.close()
        self.conn.commit()

    def close(self):
        self.conn.close()


sqlite_client = SqliteClient()
