from authlib.integrations.starlette_client import OAuth
from fastapi import HTTPException
from starlette.config import Config
from starlette.requests import Request
from app.config import settings

config = Config('.env')
oauth = OAuth(config)

oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

async def get_google_oauth_token(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to get access token")
    return token

async def get_google_user(token):
    resp = await oauth.google.parse_id_token(token)
    return resp