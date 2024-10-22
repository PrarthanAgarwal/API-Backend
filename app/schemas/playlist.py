from pydantic import BaseModel
from typing import List, Optional
from .base import ItemBase, ItemCreate, ItemInDBBase
from .track import Track

class PlaylistBase(ItemBase):
    name: str
    description: str

class PlaylistCreate(ItemCreate, PlaylistBase):
    pass

class PlaylistUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Playlist(ItemInDBBase, PlaylistBase):
    pass

class PlaylistInDB(Playlist):
    pass

class PlaylistWithTracks(Playlist):
    tracks: List[Track] = []

def update_forward_refs():
    PlaylistWithTracks.update_forward_refs()
