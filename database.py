#!/usr/bin/python
# -*- coding:utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, String, Integer, MetaData
from sqlalchemy.orm import sessionmaker
from settings import DB_PATH

engine = create_engine('sqlite:///' + DB_PATH)
db = declarative_base()


class Domain(db):
    __tablename__ = "domain"
    id = Column(Integer, primary_key=True)
    domain = Column(String(255))
    md5 = Column(String(32))
    user = Column(Integer)


class User(db):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    access_key_id = Column(String(16))
    access_key_secret = Column(String(32))


class Database(object):
    def __init__(self, verbosity = False):
        engine.echo = verbosity
        db.metadata.create_all(engine)
        self.sessionmaker = sessionmaker(bind=engine)
        self.session = self.sessionmaker()

    def add_user(self, name, access_key_id, access_key_secret):
        try:
            self.session.add(User(name=name, access_key_id=access_key_id, access_key_secret=access_key_secret))
            self.session.commit()
            print("\033[1;32mUser %s added successfully\033[0m" % name)
        except Exception:
            print(Exception)

    def add_domain(self, domain, user):
        try:
            self.session.add(Domain(domain=domain, user=user))
            self.session.commit()
            print("\033[1;32mDomain %s added successfully\033[0m" % domain)
        except Exception:
            print(Exception)

    def get_domain(self, domain):
        return self.session.query(Domain).filter(Domain.domain == domain).first()

    def get_all_domain(self):
        return self.session.query(Domain).all()

    def has_domain(self, domain):
        domain = self.get_domain(domain)
        if domain is not None:
            return True
        return False

    def has_user(self, user):
        user = self.get_user(user)
        if user is not None:
            return True
        return False

    def get_user(self, name):
        return self.session.query(User).filter(User.name == name).first()

    def get_all_user(self):
        return self.session.query(User).all()

    def update_domain(self, domain, md5, user=None):
        try:
            domain = self.session.query(Domain).filter(Domain.domain == domain).first()
            domain.md5 = md5
            if user is not None:
                domain.user = user
                print("\033[1;32mDomain %s updated successfully\033[0m" % domain)
            self.session.commit()
        except Exception:
            print(Exception)

    def delete_domain(self, domain):
        self.session.query(Domain).filter(Domain.domain == domain).delete()
        self.session.commit()
        print("\033[1;32mDomain %s deleted successfully\033[0m" % domain)

    def delete_user(self, name):
        try:
            self.session.query(User).filter(User.name == name).delete()
            self.session.commit()
            print("\033[1;32mUser %s deleted successfully\033[0m" % name)
        except Exception:
            print(Exception)




