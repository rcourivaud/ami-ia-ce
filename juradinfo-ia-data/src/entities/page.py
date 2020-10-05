from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import Sequence
from sqlalchemy.ext.declarative import declarative_base
from base.env import App


Base = declarative_base()
table_name = App.get_db_table_name()


class Page(Base):
    """
    Class that map the table of the database that containt OCR text
    """

    __tablename__ = table_name
    id = Column(Integer, Sequence("id"), primary_key=True)
    num_folder = Column(Integer)
    ta = Column(String(50))
    request_name = Column(String(100))
    page_number = Column(Integer)
    file_path = Column(String(100))
    content = Column(LONGTEXT)
    is_scan = Column(Integer)

    def __repr__(self):
        return (
            "<Page(request name='%s', folder number = %s,TA = %s,  number of pages='%s, file_path=%s,  content')>"
            % (
                self.request_name,
                str(self.num_folder),
                str(self.ta),
                str(self.page_number),
                str(self.file_path),
            )
        )
