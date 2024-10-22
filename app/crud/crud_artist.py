from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.artist import Artist as ArtistModel
from app.schemas.artist import ArtistCreate, ArtistUpdate

class CRUDArtist(CRUDBase[ArtistModel, ArtistCreate, ArtistUpdate]):
    def get_by_spotify_id(self, db: Session, *, spotify_id: str) -> Optional[ArtistModel]:
        return db.query(ArtistModel).filter(ArtistModel.spotify_id == spotify_id).first()

    def get_multi_by_name(self, db: Session, *, name: str, skip: int = 0, limit: int = 100) -> List[ArtistModel]:
        return db.query(ArtistModel).filter(ArtistModel.name.ilike(f"%{name}%")).offset(skip).limit(limit).all()

artist = CRUDArtist(ArtistModel)
