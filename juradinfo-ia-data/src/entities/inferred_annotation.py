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

    __tablename__ = "gld_inferred_annotation"
    id = Column(Integer, Sequence("id"), primary_key=True)
    categorie = Column(TEXT)
    request_id = Column(TEXT)
    selectedTerm = Column(TEXT)
    paragraph_id = Column(TEXT)


    def __init__(self, categorie, request_id, selectedTerm, paragraph_id):
        self.categorie = categorie
        self.request_id = request_id
        self.selectedTerm = selectedTerm
        self.paragraph_id = paragraph_id


    def __repr__(self):
        return "<Page(categorie = %s, request_id = %s,  paragraph_id='%s)>" % (
            self.categorie,
            self.request_id,
            str(self.paragraph_id),
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

    def save_to_db(self, session):
        session.add(self)
        session.commit()
