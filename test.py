from sqlalchemy import create_engine, text
from app.core.config import settings
import sqlalchemy

print(f"SQLAlchemy version: {sqlalchemy.__version__}")

# Create the engine
engine = create_engine(settings.DATABASE_URL, echo=True)

# Try to connect
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Connection successful!")
        print("Result:", result.fetchone())
except Exception as e:
    print("Connection failed.")
    print("Error:", str(e))
    print("Error type:", type(e))

print(f"Database URL: {settings.DATABASE_URL}")
