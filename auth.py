from jose import jwt
import time
from authlib.integrations.starlette_client import OAuth
from fastapi import Request
from config import (
    APPLE_CLIENT_ID, APPLE_TEAM_ID, APPLE_KEY_ID, APPLE_PRIVATE_KEY_PATH
)

oauth = OAuth()

def get_apple_private_key():
    with open(APPLE_PRIVATE_KEY_PATH, "r") as f:
        return f.read()

def generate_apple_client_secret():
    headers = {
        "kid": APPLE_KEY_ID,
        "alg": "ES256"
    }

    claims = {
        "iss": APPLE_TEAM_ID,
        "iat": int(time.time()),
        "exp": int(time.time()) + 86400 * 180,
        "aud": "https://appleid.apple.com",
        "sub": APPLE_CLIENT_ID,
    }

    client_secret = jwt.encode(
        claims,
        get_apple_private_key(),
        algorithm="ES256",
        headers=headers
    )
    return client_secret

oauth.register(
    name="apple",
    client_id=APPLE_CLIENT_ID,
    client_secret=generate_apple_client_secret(),
    server_metadata_url="https://appleid.apple.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email name",
        "response_mode": "form_post"
    }
)
