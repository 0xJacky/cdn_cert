#!/usr/bin/python
# -*- coding:utf-8 -*-
import sqlite3

class DB:
    def __init__(self):
        self.con = sqlite3.connect('cert.db')
        self.c = self.con.cursor()

    def query(self, sql):
        self.c.execute(sql)
        self.con.commit()

    def insert(self, domain):
        sql = "INSERT INTO cert_data VALUES (\'%s\', 'NULL')" % domain
        self.query(sql)

    def update(self, domain, md5):
        sql = 'UPDATE cert_data SET md5=\'%s\' WHERE domain=\'%s\'' % (md5, domain)
        self.query(sql)

    def delete(self, domain):
        sql = 'DELETE FROM cert_data WHERE domain=\'%s\'' % domain
        self.query(sql)

    def fetchone(self, domain):
        sql = 'SELECT * FROM cert_data WHERE domain=\'%s\'' % domain
        self.c.execute(sql)
        return self.c.fetchone()

    def domainlist(self):
        self.c.execute('SELECT `domain` FROM cert_data')
        result = ()
        for f in self.c.fetchall():
            result = result + f
        return result
