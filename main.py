# from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from auth import oauth

from database import engine, Base
from routers_profile import router as routers_profile

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-session-secret-key")

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Startup code
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     # Shutdown code (if any)
        
@app.get("/")
async def read_root():
    return {"message": "Welcome to Spartr!"}

@app.get("/api")
async def read_root():
    return {"api root": "not available for public view"}

@app.get("/api/login/apple")
async def login_via_apple(request: Request):
    redirect_uri = request.url_for("auth_via_apple")
    return await oauth.apple.authorize_redirect(request, redirect_uri)

@app.post("/api/auth/apple", name="auth_via_apple")
async def auth_via_apple(request: Request):
    try:
        token = await oauth.apple.authorize_access_token(request)
        user_info = token.get("userinfo") or {}
        id_token = token.get("id_token")

        # Decode id_token if needed (to get 'sub' = Apple's user ID)
        # Store user or create new one here

        return JSONResponse({
            "access_token": id_token,
            "user_info": user_info,
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)
