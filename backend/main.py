import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
SECRET_KEY = os.getenv("SECRET_KEY")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3001")

# Session middleware is required by Authlib for OAuth 2.0
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# CORS middleware to allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth = OAuth()
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile',
        'timeout': 30.0
    }
)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Google OAuth Backend"}

@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, str(redirect_uri))

@app.get("/auth")
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTTPException(status_code=401, detail=error.error)
    
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    
    return RedirectResponse(url=FRONTEND_URL)

@app.get("/me")
async def get_me(request: Request):
    user = request.session.get('user')
    if user:
        return user
    return JSONResponse(status_code=401, content={"message": "Not authenticated"})

@app.get("/logout")
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url=FRONTEND_URL)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)