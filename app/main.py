from fastapi import FastAPI
from app.api.v1 import tracks, artists, playlists
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(tracks.router, prefix=f"{settings.API_V1_STR}/tracks", tags=["tracks"])
app.include_router(artists.router, prefix=f"{settings.API_V1_STR}/artists", tags=["artists"])
app.include_router(playlists.router, prefix=f"{settings.API_V1_STR}/playlists", tags=["playlists"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Music Recommender API"}
