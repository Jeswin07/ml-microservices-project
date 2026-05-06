from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Request Schema
class PredictionRecord(BaseModel):
    gender: int   # 0 = male, 1 = female
    age: int
    salary: int
    prediction: int


# 🔹 DB Connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "postgres"),  # ✅ Kubernetes service name
        database="postgres",
        user="postgres",
        password="admin"
    )


# 🔹 Ensure table exists (runs once)
def create_table():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
            gender INT,
            age INT,
            salary INT,
            prediction INT
        )
    """)

    conn.commit()
    conn.close()


# 🔹 Run on startup
@app.on_event("startup")
def startup():
    create_table()


@app.get("/")
def home():
    return {"message": "History Service Running"}


# 🔹 Save Prediction
@app.post("/save")
def save_prediction(data: PredictionRecord):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO predictions (gender, age, salary, prediction)
        VALUES (%s, %s, %s, %s)
    """, (data.gender, data.age, data.salary, data.prediction))

    conn.commit()
    conn.close()

    return {"message": "Saved successfully"}


# 🔹 Get History
@app.get("/history")
def get_history():
    conn = get_db_connection()
    cur = conn.cursor()

    # ✅ Safety: ensure table exists even if startup missed
    cur.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
            gender INT,
            age INT,
            salary INT,
            prediction INT
        )
    """)

    cur.execute("SELECT * FROM predictions")
    rows = cur.fetchall()

    conn.close()

    results = []

    for row in rows:
        results.append({
            "id": row[0],
            "gender": "male" if row[1] == 0 else "female",
            "age": row[2],
            "salary": row[3],
            "prediction": row[4],
            "meaning": "Will Purchase" if row[4] == 1 else "Will Not Purchase"
        })

    return {"data": results}