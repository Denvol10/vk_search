import os


from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
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
    friends_count = Column(Integer)
    target = Column(Boolean)

    def __str__(self):
        return self.page_id

class VkPhoto(Base):
    __tablename__ = 'Photos'
    id = Column(Integer, primary_key=True)
    page_id = Column(String, ForeignKey(VkPage.id))
    photo_id = Column(String)
    count_photos = Column(Integer)

    def __str__(self):
        return self.photo_date

class VkWall(Base):
    __tablename__ = 'VkWalls'
    id = Column(Integer, primary_key=True)
    page_id = Column(String, ForeignKey(VkPage.id))
    wall_id = Column(String)
    posts_count = Column(Integer)
    likes_count = Column(Integer)
    reposts_count = Column(Integer)

    def __str__(self):
        return self.page_id


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)