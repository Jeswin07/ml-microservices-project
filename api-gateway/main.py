from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import requests
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ML_SERVICE_URL = "http://ml-service:8002"
HISTORY_SERVICE_URL = "http://history-service:8003"

SECRET_KEY = "secret123"
ALGORITHM = "HS256"

security = HTTPBearer()


# 🔹 Schema
class PredictionRequest(BaseModel):
    gender: str
    age: int
    salary: int


# 🔐 Token verification (used globally)
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/")
def home():
    return {"message": "API Gateway Running"}


# 🔥 Protected endpoint
@app.post("/predict")
def predict(request: PredictionRequest, user=Depends(verify_token)):

    # 🔹 Call ML
    response = requests.post(
        f"{ML_SERVICE_URL}/predict",
        json=request.dict()
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="ML service error")

    ml_response = response.json()

    # 🔹 Convert gender for DB
    gender_map = {"male": 0, "female": 1}
    gender_value = gender_map.get(ml_response.get("gender", "").lower())

    # 🔹 Save to history
    try:
        requests.post(
            f"{HISTORY_SERVICE_URL}/save",
            json={
                "gender": gender_value,
                "age": ml_response["age"],
                "salary": ml_response["salary"],
                "prediction": ml_response["prediction"]
            }
        )
    except:
        pass

    return ml_response


# 🔹 Protected history
@app.get("/history")
def get_history(user=Depends(verify_token)):
    response = requests.get(f"{HISTORY_SERVICE_URL}/history")
    return response.json()