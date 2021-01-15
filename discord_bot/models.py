import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Integer, String, Column
from sqlalchemy import create_engine

Base = declarative_base()

engine = create_engine(os.environ["DATABASE_URL"])

Session = sessionmaker()
Session.configure(bind=engine)


class GameInfo(Base):
    """Information about a game we're tracking."""
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    itad_plain = Column(String)

    def __repr__(self):
        return f"<GameInfo name='${self.name}' plain='${self.itad_plain}'>"
