#!/usr/bin/python
# -*- coding:utf-8 -*-
from sqlalchemy import *
from settings import DB_PATH

class DB:
    def __init__(self):
        self.db = create_engine('sqlite:///'+DB_PATH)
        self.db.echo = False
        self.conn = self.db.connect()
        self.metadata = MetaData(self.db)
        if not self.db.dialect.has_table(self.db, 'cert_data'):
            self.init()
        self.data = Table('cert_data',
                        self.metadata,
                        autoload=True)


    def query(self, sql):
        self.c.execute(sql)
        self.con.commit()

    def add(self):
        i = self.data.insert()
        domain = raw_input('Plase input the domain name, use \',\' to split.\n')
        d = ()
        if ',' in domain:
            domain_list = domain.split(',')
            for k in domain_list:
                t = {}
                t['domain'] = k
                t['md5'] = ''
                d = d + (t,)
        else:
            t = {}
            t['domain'] = domain
            t['md5'] = ''
            d = d + (t,)
        try:
            i.execute(d)
            print "Execute successfully."
        except Exception:
            print Exception

    def update(self, domain, md5):
        query = self.data.update().where(self.data.c.domain == domain).values({'md5': md5})
        self.conn.execute(query)

    def delete(self):
        domain = raw_input('Plase input a domain name to delete.\n')
        query = self.data.delete().where(self.data.c.domain == domain)
        try:
            self.conn.execute(query)
            print "Execute successfully."
        except Exception:
            print Exception

    def fetchone(self, domain):
        query = self.data.select().where(self.data.c.domain == domain)
        return self.conn.execute(query).fetchone()

    def fetchall(self):
        s = self.data.select()
        r = s.execute()
        output = ()
        for f in r.fetchall():
            output = output + (f[0],)
        return output

    def domainlist(self):
        s = self.data.select()
        r = s.execute()
        print "CDN Cert -- Domain List"
        print "-----------------------"
        for f in r.fetchall():
            print f[0]
        print "-----------------------"

    def intable(self, domain):
        if self.fetchone(domain=domain):
            return True
        else:
            return False

    def init(self):
        table = (
            ('cert_data',
                (
                    Column('domain', String(255), unique=True),
                    Column('md5', String(32)),
                ),
            ),
        )
        metadata = MetaData(self.db)

        for name, columns in table:
            try:
                c_table = Table(name, metadata, autoload=True)
            except:
                c_table = apply(Table, (name, metadata) + columns)
                c_table.create()
        print 'Database has been initialized'
