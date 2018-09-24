#!/usr/bin/python3

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False)

    # Make sure we don't create duplicate user records
    @classmethod
    def get_unique(cls, session, username):
        cache = session._unique_cache = getattr(session, '_unique_cache', {})
        key = (cls, username)
        o = cache.get(key)
        if o is None:
            # check the database if it's not in the cache
            o = session.query(cls).filter_by(username=username).first()
            if o is None:
                # create a new one if it's not in the database
                o = cls(username=username)
                session.add(o)
            # update the cache
            cache[key] = o
        return o

class Usage(Base):
    __tablename__ = "usage"
    id = Column(Integer, primary_key=True)
    start_time = Column(Integer, nullable=False)
    end_time = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
