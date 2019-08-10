import sqlite3

from application.config import BLACKLIST_TABLENAME, BLACKLIST_SQL, CONFIG_SQL, CONFIG_TABLENAME, BLACKLIST_DBNAME, \
    CONFIG_DBNAME


class SqliteClient:
    def __init__(self, db_name, tablename, sql):
        self.conn = sqlite3.connect(db_name + '.db')
        self.tablename = tablename
        self.create(sql)

    def create(self, sql):
        cursor = self.conn.cursor()
        y = cursor.execute(f"select count(*) from sqlite_master where type ='table' and name ='{self.tablename}'")
        if y.fetchone()[0] > 0:
            return
        cursor.execute(sql)
        cursor.close()
        self.conn.commit()

    def query_all(self, *args):
        cursor = self.conn.cursor()
        res = cursor.execute(f'select {args[0]} from {self.tablename}')
        return res.fetchall()

    def query(self, *args, **kwargs):
        cursor = self.conn.cursor()
        res = cursor.execute(
            f'select {args[0]} from {self.tablename} where {list(kwargs.keys())[0]} = "{list(kwargs.values())[0]}"')
        return res.fetchall()

    def load_ip(self):
        res = self.query_all('ip')
        data = set()
        for i in res:
            data.add(i[0])
        return data

    def load_config(self):
        pass

    def push(self, **kwargs):
        cursor = self.conn.cursor()
        cursor.execute(f'insert into {self.tablename} ({list(kwargs.keys())[0]}) values ("{list(kwargs.values())[0]}")')
        cursor.close()
        self.conn.commit()

    def pop(self, **kwargs):
        cursor = self.conn.cursor()
        cursor.execute(f'delete from {self.tablename} where {list(kwargs.keys())[0]} = "{list(kwargs.values())[0]}"')
        cursor.close()
        self.conn.commit()

    def close(self):
        self.conn.close()


blacklist_db = SqliteClient(db_name=BLACKLIST_DBNAME, tablename=BLACKLIST_TABLENAME, sql=BLACKLIST_SQL)
config_db = SqliteClient(db_name=CONFIG_DBNAME, tablename=CONFIG_TABLENAME, sql=CONFIG_SQL)
