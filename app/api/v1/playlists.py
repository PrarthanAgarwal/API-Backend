from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.db.base import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Playlist])
def read_playlists(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    playlists = crud.playlist.get_multi(db, skip=skip, limit=limit)
    return playlists

@router.post("/", response_model=schemas.Playlist)
def create_playlist(
    *,
    db: Session = Depends(deps.get_db),
    playlist_in: schemas.PlaylistCreate,
):
    playlist = crud.playlist.create(db=db, obj_in=playlist_in)
    return playlist

@router.get("/{playlist_id}", response_model=schemas.PlaylistWithTracks)
def read_playlist(
    *,
    db: Session = Depends(deps.get_db),
    playlist_id: int,
):
    playlist = crud.playlist.get(db=db, id=playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return playlist

@router.put("/{playlist_id}", response_model=schemas.Playlist)
def update_playlist(
    *,
    db: Session = Depends(deps.get_db),
    playlist_id: int,
    playlist_in: schemas.PlaylistUpdate,
):
    playlist = crud.playlist.get(db=db, id=playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    playlist = crud.playlist.update(db=db, db_obj=playlist, obj_in=playlist_in)
    return playlist

@router.delete("/{playlist_id}", response_model=schemas.Playlist)
def delete_playlist(
    *,
    db: Session = Depends(deps.get_db),
    playlist_id: int,
):
    playlist = crud.playlist.get(db=db, id=playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    playlist = crud.playlist.remove(db=db, id=playlist_id)
    return playlist

@router.post("/{playlist_id}/tracks/{track_id}")
def add_track_to_playlist(playlist_id: int, track_id: int, db: Session = Depends(get_db)):
    db_playlist = crud.playlist.get(db, id=playlist_id)
    if db_playlist is None:
        raise HTTPException(status_code=404, detail="Playlist not found")
    db_track = crud.track.get(db, id=track_id)
    if db_track is None:
        raise HTTPException(status_code=404, detail="Track not found")
    db_playlist.tracks.append(db_track)
    db.commit()
    return {"message": "Track added to playlist"}
