from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.api.deps import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Track])
def read_tracks(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    tracks = crud.track.get_multi(db, skip=skip, limit=limit)
    return tracks

@router.post("/", response_model=schemas.Track)
def create_track(
    *,
    db: Session = Depends(deps.get_db),
    track_in: schemas.TrackCreate,
):
    track = crud.track.create(db=db, obj_in=track_in)
    return track

@router.get("/{track_id}", response_model=schemas.TrackWithArtist)
def read_track(
    *,
    db: Session = Depends(deps.get_db),
    track_id: int,
):
    track = crud.track.get(db=db, id=track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return track

@router.put("/{track_id}", response_model=schemas.Track)
def update_track(
    *,
    db: Session = Depends(deps.get_db),
    track_id: int,
    track_in: schemas.TrackUpdate,
):
    track = crud.track.get(db=db, id=track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    track = crud.track.update(db=db, db_obj=track, obj_in=track_in)
    return track

@router.delete("/{track_id}", response_model=schemas.Track)
def delete_track(
    *,
    db: Session = Depends(deps.get_db),
    track_id: int,
):
    track = crud.track.get(db=db, id=track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    track = crud.track.remove(db=db, id=track_id)
    return track

@router.post("/{playlist_id}/tracks/{track_id}")
def add_track_to_playlist(
    playlist_id: int, 
    track_id: int, 
    db: Session = Depends(deps.get_db)  # Change this line
):
    db_playlist = crud.playlist.get(db, id=playlist_id)
    if db_playlist is None:
        raise HTTPException(status_code=404, detail="Playlist not found")
    db_track = crud.track.get(db, id=track_id)
    if db_track is None:
        raise HTTPException(status_code=404, detail="Track not found")
    db_playlist.tracks.append(db_track)
    db.commit()
    return {"message": "Track added to playlist"}
