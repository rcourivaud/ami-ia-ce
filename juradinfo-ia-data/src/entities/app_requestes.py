from sqlalchemy import Column, Integer, String, DateTime, TEXT, Float

# from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy import Sequence
from sqlalchemy.ext.declarative import declarative_base
from base.env import App
from sqlalchemy.sql import select


Base = declarative_base()


class Request(Base):
    """
    Class that map the table of the database that containt OCR text
    """

    __tablename__ = "app_requetes_copy"
    index = Column(Integer, Sequence("id"), primary_key=True)
    request_id = Column(TEXT)
    num_dossier = Column(Integer, primary_key=True)
    ta = Column(TEXT)
    ta_code = Column(TEXT)
    request_name = Column(TEXT)
    date_enreg = Column(DateTime, primary_key=True)
    content = Column(TEXT, primary_key=True)
    matiere = Column(TEXT)
    titre = Column(TEXT)
    tete_serie = Column(Float, primary_key=True)
    num_serie = Column(TEXT)
    nom_serie = Column(TEXT)
    file_path = Column(TEXT)
    nb_pages = Column(Integer, primary_key=True)
    is_scan = Column(Integer, primary_key=True)
    fichier_meta_donnee_CE = Column(TEXT)
    statut_annotation = Column(Integer, primary_key=True)

    def __init__(
        self,
        request_id,
        num_dossier,
        ta,
        ta_code,
        request_name,
        date_enreg,
        content,
        matiere,
        titre,
        tete_serie,
        num_serie,
        nom_serie,
        file_path,
        nb_pages,
        is_scan,
        fichier_meta_donnee_CE,
        statut_annotation,
    ):
        self.request_index = request_id
        self.num_dossier = num_dossier
        self.ta = ta
        self.ta_code = ta_code
        self.request_name = request_name
        self.date_enreg = date_enreg
        self.content = content
        self.matiere = matiere
        self.titre = titre
        self.tete_serie = tete_serie
        self.num_serie = num_serie
        self.nom_serie = nom_serie
        self.file_path = file_path
        self.nb_pages = nb_pages
        self.is_scan = is_scan
        self.fichier_meta_donnee_CE = fichier_meta_donnee_CE
        self.statut_annotation = statut_annotation

    @classmethod
    def find_by_id(cls, engine, rq_id):
        conn = engine.connect()

        stmt = select([cls]).where(cls.request_id == rq_id)
        results = conn.execute(stmt)

        return results

    @classmethod
    def find_distinct_id(cls, engine):
        conn = engine.connect()

        stmt = select([cls.request_id]).distinct()
        results = conn.execute(stmt).fetchall()

        return results

    @classmethod
    def find_all_requests_id(cls, engine):
        conn = engine.connect()

        stmt = select([cls.request_id]).distinct()
        results = conn.execute(stmt).fetchall()

        return results
