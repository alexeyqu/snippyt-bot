#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

DeclarativeBase = declarative_base()


class PySession(DeclarativeBase):
    __tablename__ = 'pysession'

    id = Column('id', Integer, primary_key=True)
    owner = Column('owner', String, nullable=False)
    code = Column('code', UnicodeText)

    def __repr__(self):
        return "<Session({0}, {1})>".format(self.id, self.owner)


class Storage:
    def __init__(self, db_path):
        self.dbengine = create_engine(
            'sqlite:///{}'.format(db_path), echo=True
        )
        DeclarativeBase.metadata.create_all(self.dbengine)
        Session = sessionmaker(bind=self.dbengine)
        self.session = Session()

    def get_session(self, user, session_id):
        res = self.session.query(PySession).filter_by(id=session_id)
        if not res:
            raise LookupError(
                'No session {} for {}'.format(session_id, user)
            )
        pysess = res.first()
        assert user == pysess.owner
        return pysess.code

    def store_session(self, user, session_id, code):
        if session_id is None:
            pysess = PySession(owner=user, code=code)
            self.session.add(pysess)
        else:
            pysess = PySession(id=session_id, owner=user, code=code)
            self.session.merge(pysess)
        self.session.commit()
        return pysess.id
