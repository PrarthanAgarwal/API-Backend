from pydantic import BaseModel
from typing import List, Optional
from .base import ItemBase, ItemCreate, ItemInDBBase

class ArtistBase(ItemBase):
    name: str
    spotify_id: str

class ArtistCreate(ItemCreate, ArtistBase):
    pass

class ArtistUpdate(BaseModel):
    name: Optional[str] = None
    spotify_id: Optional[str] = None

class Artist(ItemInDBBase, ArtistBase):
    pass

class ArtistInDB(Artist):
    pass

class ArtistWithTracks(Artist):
    tracks: Optional[List['Track']] = None

from .track import Track
ArtistWithTracks.update_forward_refs()

def update_forward_refs():
    ArtistWithTracks.update_forward_refs()
