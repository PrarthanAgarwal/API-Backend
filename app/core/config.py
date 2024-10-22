from pydantic import BaseSettings, PostgresDsn

class Settings(BaseSettings):
    PROJECT_NAME: str = "Music Recommender API"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: PostgresDsn
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str

    class Config:
        env_file = ".env"

settings = Settings()

