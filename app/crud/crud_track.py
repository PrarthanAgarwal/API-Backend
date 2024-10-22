from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.db.base import get_db
from app.crud.base import CRUDBase
from app.models.track import Track as TrackModel
from app.schemas.track import TrackCreate, TrackUpdate

router = APIRouter()

@router.get("/", response_model=List[schemas.Artist])
def read_artists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    artists = crud.artist.get_multi(db, skip=skip, limit=limit)
    return artists

@router.post("/", response_model=schemas.Artist)
def create_artist(artist: schemas.ArtistCreate, db: Session = Depends(get_db)):
    return crud.artist.create(db=db, obj_in=artist)

@router.get("/{artist_id}", response_model=schemas.Artist)
def read_artist(artist_id: int, db: Session = Depends(get_db)):
    db_artist = crud.artist.get(db, id=artist_id)
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return db_artist

@router.put("/{artist_id}", response_model=schemas.Artist)
def update_artist(artist_id: int, artist: schemas.ArtistUpdate, db: Session = Depends(get_db)):
    db_artist = crud.artist.get(db, id=artist_id)
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return crud.artist.update(db=db, db_obj=db_artist, obj_in=artist)

@router.delete("/{artist_id}", response_model=schemas.Artist)
def delete_artist(artist_id: int, db: Session = Depends(get_db)):
    db_artist = crud.artist.get(db, id=artist_id)
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return crud.artist.remove(db=db, id=artist_id)

class CRUDTrack(CRUDBase[TrackModel, TrackCreate, TrackUpdate]):
    def get_by_spotify_id(self, db: Session, *, spotify_id: str) -> Optional[TrackModel]:
        return db.query(TrackModel).filter(TrackModel.spotify_id == spotify_id).first()

    def get_multi_by_artist(self, db: Session, *, artist_id: int, skip: int = 0, limit: int = 100) -> List[TrackModel]:
        return db.query(TrackModel).filter(TrackModel.artist_id == artist_id).offset(skip).limit(limit).all()

track = CRUDTrack(TrackModel)
