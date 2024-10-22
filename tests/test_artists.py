from sqlalchemy import create_engine, text
from app.core.config import settings
import sqlalchemy

print(f"SQLAlchemy version: {sqlalchemy.__version__}")

# Create the engine
engine = create_engine(settings.DATABASE_URL, echo=True)

# Try to connect and test artist-related operations
try:
    with engine.connect() as connection:
        # Test creating an artist
        connection.execute(text("INSERT INTO artists (name, spotify_id, popularity) VALUES ('Test Artist', 'test123', 50)"))
        
        # Test retrieving an artist
        result = connection.execute(text("SELECT * FROM artists WHERE name = 'Test Artist'"))
        artist = result.fetchone()
        print("Artist created and retrieved successfully!")
        print("Artist:", artist)
        
        # Clean up: delete the test artist
        connection.execute(text("DELETE FROM artists WHERE name = 'Test Artist'"))
        
        print("Artist test operations completed successfully!")
except Exception as e:
    print("Artist test operations failed.")
    print("Error:", str(e))
    print("Error type:", type(e))

print(f"Database URL: {settings.DATABASE_URL}")

