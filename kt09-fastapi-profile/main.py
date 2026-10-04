import hashlib
import secrets

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="Profile API")
USERS = {}
TOKENS = {}


class RegisterIn(BaseModel):
    username: str = Field(min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(min_length=8)
    email: EmailStr
    name: str = Field(min_length=1, max_length=80)


class LoginIn(BaseModel):
    username: str
    password: str


class ProfileUpdate(BaseModel):
    email: EmailStr | None = None
    name: str | None = Field(default=None, min_length=1, max_length=80)


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000).hex()


def issue_token(username):
    token = secrets.token_urlsafe(24)
    TOKENS[token] = username
    return {"access_token": token, "token_type": "bearer"}


def current_user(authorization: str = Header(default="")):
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or token not in TOKENS:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing token")
    return USERS[TOKENS[token]]


def public(user):
    return {"username": user["username"], "email": user["email"], "name": user["name"]}


@app.post("/api/register", status_code=status.HTTP_201_CREATED)
async def register(data: RegisterIn):
    if data.username.lower() in USERS:
        raise HTTPException(status.HTTP_409_CONFLICT, "Username already taken")
    salt = secrets.token_hex(8)
    USERS[data.username.lower()] = {"username": data.username, "email": data.email, "name": data.name, "salt": salt, "hash": hash_password(data.password, salt)}
    return issue_token(data.username.lower())


@app.post("/api/login")
async def login(data: LoginIn):
    user = USERS.get(data.username.lower())
    if not user or not secrets.compare_digest(user["hash"], hash_password(data.password, user["salt"])):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong username or password")
    return issue_token(data.username.lower())


@app.get("/api/profile")
async def get_profile(user=Depends(current_user)):
    return public(user)


@app.patch("/api/profile")
async def update_profile(data: ProfileUpdate, user=Depends(current_user)):
    for key, value in data.model_dump(exclude_none=True).items():
        user[key] = value
    return public(user)


@app.post("/api/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(authorization: str = Header(default=""), user=Depends(current_user)):
    TOKENS.pop(authorization.partition(" ")[2], None)
