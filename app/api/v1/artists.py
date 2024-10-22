from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.api.deps import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Artist])
def read_artists(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    artists = crud.artist.get_multi(db, skip=skip, limit=limit)
    return artists

@router.post("/", response_model=schemas.Artist)
def create_artist(
    *,
    db: Session = Depends(deps.get_db),
    artist_in: schemas.ArtistCreate,
):
    artist = crud.artist.create(db=db, obj_in=artist_in)
    return artist

@router.get("/{artist_id}", response_model=schemas.ArtistWithTracks)
def read_artist(
    *,
    db: Session = Depends(deps.get_db),
    artist_id: int,
):
    artist = crud.artist.get(db=db, id=artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist

@router.put("/{artist_id}", response_model=schemas.Artist)
def update_artist(
    *,
    db: Session = Depends(deps.get_db),
    artist_id: int,
    artist_in: schemas.ArtistUpdate,
):
    artist = crud.artist.get(db=db, id=artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    artist = crud.artist.update(db=db, db_obj=artist, obj_in=artist_in)
    return artist

@router.delete("/{artist_id}", response_model=schemas.Artist)
def delete_artist(
    *,
    db: Session = Depends(deps.get_db),
    artist_id: int,
):
    artist = crud.artist.get(db=db, id=artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    artist = crud.artist.remove(db=db, id=artist_id)
    return artist
