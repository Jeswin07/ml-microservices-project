from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()

SECRET_KEY = "secret123"
ALGORITHM = "HS256"

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔐 Swagger security (lock icon)
security = HTTPBearer()

# 🧠 Fake DB (in-memory)
users_db = {}

# 🔹 Schemas
class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str


# 🔹 Register
@app.post("/register")
def register(data: RegisterRequest):
    if data.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    users_db[data.username] = data.password
    return {"message": "User registered successfully"}


# 🔹 Login
@app.post("/login")
def login(data: LoginRequest):
    user = users_db.get(data.username)

    if not user or user != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({
        "sub": data.username,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token}


# 🔹 Protected test endpoint 
@app.get("/me")
def get_me(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"user": payload["sub"]}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")