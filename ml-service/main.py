from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
import joblib
import numpy as np

app = FastAPI()

model = joblib.load("model.pkl")

# Schema
class PredictionRequest(BaseModel):
    gender: str
    age: int
    salary: int

class PredictionResponse(BaseModel):
    gender: str
    age: int
    salary: int
    prediction: int
    meaning: str

@app.get("/")
def home():
    return {"message": "ML Service Running"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    gender_map = {"male": 0, "female": 1}

    gender = gender_map.get(request.gender.lower())

    if gender is None :
        raise HTTPException(
            status_code=400,
            detail="Invalid gender. Use 'male' or 'female'"
        )

    try:
        data = np.array([[gender, request.age, request.salary]])
        prediction = model.predict(data)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "gender": request.gender.lower(),
        "age": request.age,
        "salary": request.salary,
        "prediction": int(prediction),
        "meaning": "Will Purchase" if prediction == 1 else "Will Not Purchase"
    }