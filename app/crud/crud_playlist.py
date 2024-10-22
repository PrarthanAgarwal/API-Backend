from app.crud.base import CRUDBase
from app.models.playlist import Playlist
from app.schemas.playlist import PlaylistCreate, PlaylistUpdate

class CRUDPlaylist(CRUDBase[Playlist, PlaylistCreate, PlaylistUpdate]):
    pass

playlist = CRUDPlaylist(Playlist)

