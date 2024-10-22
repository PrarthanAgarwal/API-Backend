from .track import Track, TrackCreate, TrackInDB, TrackWithArtist, TrackUpdate
from .artist import Artist, ArtistCreate, ArtistInDB, ArtistWithTracks, ArtistUpdate
from .playlist import Playlist, PlaylistCreate, PlaylistInDB, PlaylistWithTracks, PlaylistUpdate

__all__ = [
    "Track", "TrackCreate", "TrackInDB", "TrackWithArtist", "TrackUpdate",
    "Artist", "ArtistCreate", "ArtistInDB", "ArtistWithTracks", "ArtistUpdate",
    "Playlist", "PlaylistCreate", "PlaylistInDB", "PlaylistWithTracks", "PlaylistUpdate"
]

# Update forward references
from .track import update_forward_refs as update_track_forward_refs
from .artist import update_forward_refs as update_artist_forward_refs
from .playlist import update_forward_refs as update_playlist_forward_refs

update_track_forward_refs()
update_artist_forward_refs()
update_playlist_forward_refs()
