"""Declare models and relationships."""
from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from Crypto import Random
from Crypto.Cipher import AES
from utils import dbPostgresGetEngine

engine = dbPostgresGetEngine()
Base = declarative_base()
class Article(Base):
    """Article."""
    __tablename__ = "Article"
    slug_id = Column(String(255), primary_key=True)
    article_date = Column(DateTime, unique=False, nullable=False)
    title = Column(String(255), nullable=False)
    section = Column(String(255), unique=False, nullable=False)
    subsection = Column(String(255))
    url = Column(String(5000))
    webPageAvailability = Column(String(1))
    apiInvokeDate = Column(DateTime)
 
    def __repr__(self):
        return "<articles %r>" % self.title

class Author(Base):
    """Author."""
    __tablename__ = "Author"
    id = Column(Integer, primary_key = True, autoincrement=True)
    slug_id = Column(String(255), ForeignKey("Article.slug_id"), nullable=False)
    fullname = Column(String(255), nullable=False)
 
    def __repr__(self):
        return "<author %r>" % self.fullname


Base.metadata.create_all(engine)