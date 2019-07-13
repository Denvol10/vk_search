import os

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

basedir = os.path.abspath(os.path.dirname(__file__))

engine = create_engine('sqlite:///' + os.path.join(basedir, 'vk_data.db'))

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class VkPage(Base):
    __tablename__ = 'VkPages'
    id = Column(Integer, primary_key=True)
    page_id = Column(String, unique=True)
    pagename = Column(String)

    def __str__(self):
        return self.page_id

class VkPhoto(Base):
    __tablename__ = 'Photos'
    id = Column(Integer, primary_key=True)
    page_id = Column(String, ForeignKey(VkPage.id))
    photo_date = Column(Integer)

    def __str__(self):
        return self.photo_date

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)




