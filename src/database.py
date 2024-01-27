# -*- coding: utf-8 -*-
"""
All Database models are defined here
All Database helper functions are defined here
"""
from datetime import datetime
from typing import List

from fastapi import Request
from sqlalchemy import Boolean, Column, create_engine, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.mysql import CHAR, TEXT, TINYINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

import config
import constants
import helpers

# import models
from logger import logger
from src.models import basemodel, request

Base = declarative_base()


###### INITIALIZE #######
class DatabaseFactory:
    """Implements a database factory pattern to initialize a database connection"""

    def __init__(self, settings: config.Config):
        # dsn connection string from settings
        logger.info(
            "Initializing database. HOST: %s, PORT: %s, DB: %s", settings.db_host, settings.db_port, settings.db_name
        )
        database_url = "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(
            settings.db_user,
            settings.db_pwd,
            settings.db_host,
            settings.db_port,
            settings.db_name,
        )
        self.engine = create_engine(
            database_url, pool_pre_ping=True, pool_recycle=3600, pool_size=10, max_overflow=200
        )  # max_overflow=10?
        # will be used to opena session on every request at middleware level
        self.session_local = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )  # TODO: choose autoflush=True ?
        # Create All Databases through SQLAlchemy
        # TODO: How to handle with Alembic migrations
        Base.metadata.create_all(bind=self.engine)

        # check connection
        try:
            self.engine.connect()
        except Exception as e:
            logger.error("error - %s", e)
            raise e

    def get_session(self):
        """Create new session on every request"""
        db = self.session_local()
        logger.info(f"DB session created. Current Connection Pool Number: {self.engine.pool.checkedout()}")
        try:
            yield db
        except Exception as exc:
            db.rollback()
            logger.error("DB session error: %s", exc)
            raise exc
        # finally:
        #     # logger.debug(f"DB - closing session")
        #     db.close()
        #     logger.debug(f"DB session closed.")


# Dependency
def get_db(req: Request) -> Session:
    """db dependency injector function"""
    return next(req.state.db)


######### DB Models ###########


class User(Base):
    """
    ORM Model for users table - Should be read only
    This module is used to validate
        - user <-> device relationship through user_device_mapping table
        - user <-> job relationship and authorization
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    image_url = Column(String(255))
    introduction = Column(TEXT)
    zipcode = Column(Integer)
    email_verified = Column(TINYINT)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_onboarded = Column(TINYINT)
    locale = Column(String(10))
    currency = Column(CHAR(3))

class LaterCategory(Base):
    """
    ORM Model for later_category table
    """

    __tablename__ = "later_category"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class LaterTags(Base):
    """
    ORM Model for later_tags table
    """

    __tablename__ = "later_tags"
    id = Column(Integer, primary_key=True)
    later_id = Column(Integer, ForeignKey("later.id"))
    tag = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Later(Base):
    """
    ORM Model for later table
    """

    __tablename__ = "later"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("later_category.id"))
    link = Column(String(255))
    title = Column(String(255))
    description = Column(TEXT)
    later_type = Column(Enum(constants.LaterType))
    status = Column(Enum(constants.LaterStatus))
    archived = Column(TINYINT)
    is_deleted = Column(TINYINT)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Schedule(Base):
    """
    ORM Model for schedule table
    """

    __tablename__ = "schedule"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    later_id = Column(Integer, ForeignKey("later.id"))
    schedule_start = Column(DateTime)
    schedule_end = Column(DateTime)
    status = Column(Enum(constants.ScheduleStatus))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Reminders(Base):
    """
    ORM Model for reminders table
    """

    __tablename__ = "reminders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    later_id = Column(Integer, ForeignKey("later.id"))
    reminder_time = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)