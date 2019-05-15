import sqlite3
import os

from source.StaticMethods import StaticMethods


class BDWorker:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.initialize()

    def initialize(self):
        if not os.path.exists('database.db'):
            self.conn = sqlite3.connect("database.db")
            self.cursor = self.conn.cursor()
            self.cursor.execute("""CREATE TABLE data
                              (id INTEGER PRIMARY KEY AUTOINCREMENT, post_id INTEGER, group_id INTEGER, photo_md5 text, post_date text)
                           """)
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()

    def add_post(self, post_id, post_date, group_id, photo_md5):
        self.cursor.execute("""INSERT INTO data (post_id, group_id, photo_md5, post_date)
                          VALUES ({}, {}, '{}', '{}')""".format(post_id, group_id, photo_md5, post_date))
        self.conn.commit()

    def getter(self, post_id, group_id):
        return self.cursor.execute(
            """SELECT * FROM data WHERE post_id={} and group_id={}""".format(post_id, group_id)).fetchall()

    def check_photo(self, photo):
        md5 = StaticMethods.get_md5(photo)
        return self.cursor.execute(
            """SELECT * FROM data WHERE photo_md5='{}'""".format(md5)).fetchall()
