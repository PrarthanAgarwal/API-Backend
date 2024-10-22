import logging
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from jose import JWTError, jwt
from datetime import datetime, timedelta
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from functools import wraps 

from app.config import settings
from app.models.user import Base, User
from app.auth.oauth import oauth, get_google_oauth_token, get_google_user
from app.auth.dependencies import get_current_user

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Outgoing response: {response.status_code}")
    return response

# Database setup
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

def role_required(allowed_roles):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not current_user or current_user.role not in allowed_roles:
                raise HTTPException(status_code=403, detail="Not authorized")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the API"}

@app.get("/login/google")
async def login_google(request: Request):
    logger.info("Google login initiated")
    redirect_uri = request.url_for('auth_google')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/google")
async def auth_google(request: Request, db: Session = Depends(get_db)):
    logger.info("Google authentication callback received")
    try:
        token = await get_google_oauth_token(request)
        user_data = await get_google_user(token)
        
        user = db.query(User).filter(User.email == user_data['email']).first()
        if not user:
            logger.info(f"Creating new user: {user_data['email']}")
            user = User(email=user_data['email'], name=user_data['name'])
            db.add(user)
            db.commit()
            db.refresh(user)
        
        access_token = create_access_token(data={"sub": user.email})
        logger.info(f"Authentication successful for user: {user.email}")
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Error during Google authentication: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail="Authentication failed")
    
@app.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out successfully"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    logger.info(f"User info requested for: {current_user.email}")
    return {"email": current_user.email, "name": current_user.name}

@app.get("/admin")
@role_required(['admin'])
async def admin_only(current_user: User = Depends(get_current_user)):
    return {"message": "Welcome to the admin area"}

@app.get("/manager")
@role_required(['manager', 'admin'])
async def manager_and_admin(current_user: User = Depends(get_current_user)):
    return {"message": "Welcome to the manager area"}

if __name__ == "__main__":
    logger.info("Application startup")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
