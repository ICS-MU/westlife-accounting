#!/usr/bin/python3

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from db_declarative import Base, User, Usage
from configuration import Configuration

class Database:
    def __init__(self):
        config = Configuration()
        db = config.get("db_endpoint")
        if db is None:
            logging.error("The configuration doesn't specify the DB endpoint")
            raise Exception("DB isn not given")

        self.engine = create_engine(db)
        Base.metadata.bind = self.engine
        self.DBSession = sessionmaker(bind=self.engine)

    def create(self):
        Base.metadata.create_all(self.engine)

    def store_ur(self, ur):
        session = self.DBSession()

        user = User.get_unique(session, username=ur.user)
        session.add(user)

        usage = Usage(start_time=ur.startTime, end_time=ur.endTime, user=user)
        session.add(usage)
        session.commit()
