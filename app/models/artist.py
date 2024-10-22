from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base
from pydantic import BaseModel
from typing import List, Optional

from .track import Track

class ArtistBase(BaseModel):
    name: str
    spotify_id: str
    popularity: int

class ArtistCreate(ArtistBase):
    pass

class ArtistUpdate(BaseModel):
    name: Optional[str] = None

class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    spotify_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    popularity = Column(Integer)

    tracks = relationship("Track", back_populates="artist")

    class Config:
        orm_mode = True

class ArtistWithTracks(Artist):
    tracks: List['Track']

    class Config:
        orm_mode = True

# Update forward references
ArtistWithTracks.update_forward_refs()
