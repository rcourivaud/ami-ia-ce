from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy import Sequence
from sqlalchemy.ext.declarative import declarative_base
from base.env import App
from sqlalchemy.sql import select
from sqlalchemy import asc

Base = declarative_base()


class Annotation(Base):
    """
    Class that map the table of the database that containt OCR text
    """

    __tablename__ = "app_annotation_copy"
    categorie = Column(TEXT)
    request_id = Column(TEXT)
    request_name = Column(TEXT)
    selectedTerm = Column(TEXT)
    startPos = Column(Integer, primary_key=True)
    endPos = Column(Integer, primary_key=True)
    username = Column(TEXT)

    def __init__(
        self,
        categorie,
        request_id,
        request_name,
        selectedTerm,
        startPos,
        endPos,
        username,
    ):
        self.categorie = categorie
        self.request_id = request_id
        self.request_name = request_name
        self.selectedTerm = selectedTerm
        self.startPos = startPos
        self.endPos = endPos
        self.username = username

    def __repr__(self):
        return (
            "<Page(categorie='%s', request_id = %s,request_name = %s,  startPos='%s, endPos=%s,  username=')>"
            % (
                self.categorie,
                self.request_id,
                str(self.request_name),
                str(self.startPos),
                str(self.endPos),
                str(self.username),
            )
        )

    @classmethod
    def find_all(cls, engine):
        conn = engine.connect()

        stmt = select([cls]).order_by(asc(cls.startPos))
        results = conn.execute(stmt)

        return results

    @classmethod
    def find_distinct_request_id(cls, engine):
        conn = engine.connect()

        stmt = select([cls.request_id]).distinct()
        results = conn.execute(stmt).fetchall()

        return results

    @classmethod
    def find_by_request_id(cls, engine, rq_id):
        conn = engine.connect()

        stmt = select([cls]).where(cls.request_id == rq_id).order_by(asc(cls.startPos))
        results = conn.execute(stmt)

        return results
