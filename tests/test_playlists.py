from sqlalchemy import create_engine, text
from app.core.config import settings
import sqlalchemy

print(f"SQLAlchemy version: {sqlalchemy.__version__}")

# Create the engine
engine = create_engine(settings.DATABASE_URL, echo=True)

# Try to connect and test playlist-related operations
try:
    with engine.connect() as connection:
        # Test creating a playlist
        connection.execute(text("INSERT INTO playlists (name, description, user_id) VALUES ('Test Playlist', 'A test playlist', 1)"))
        
        # Test retrieving a playlist
        result = connection.execute(text("SELECT * FROM playlists WHERE name = 'Test Playlist'"))
        playlist = result.fetchone()
        print("Playlist created and retrieved successfully!")
        print("Playlist:", playlist)
        
        # Clean up: delete the test playlist
        connection.execute(text("DELETE FROM playlists WHERE name = 'Test Playlist'"))
        
        print("Playlist test operations completed successfully!")
except Exception as e:
    print("Playlist test operations failed.")
    print("Error:", str(e))
    print("Error type:", type(e))

print(f"Database URL: {settings.DATABASE_URL}")

