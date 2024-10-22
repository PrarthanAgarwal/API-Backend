from pydantic import BaseModel
from typing import Optional
from .base import ItemBase, ItemCreate, ItemInDBBase

class TrackBase(ItemBase):
    name: str
    spotify_id: str
    album: str
    duration_ms: int
    popularity: int

class TrackCreate(ItemCreate, TrackBase):
    artist_id: int

class TrackUpdate(BaseModel):
    name: Optional[str] = None
    album: Optional[str] = None
    duration_ms: Optional[int] = None
    popularity: Optional[int] = None
    artist_id: Optional[int] = None

class Track(ItemInDBBase, TrackBase):
    artist_id: int

class TrackInDB(Track):
    pass

class TrackWithArtist(Track):
    artist: Optional['Artist'] = None

from .artist import Artist
TrackWithArtist.update_forward_refs()

def update_forward_refs():
    TrackWithArtist.update_forward_refs()
