from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    spotify_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    album = Column(String)
    duration_ms = Column(Integer)
    popularity = Column(Integer)

    artist = relationship("Artist", back_populates="tracks")
