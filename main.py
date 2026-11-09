
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import json

app = FastAPI()


# Pydantic Model
class Patient(BaseModel):
    id: str
    name: str
    city: str
    age: int
    gender: str
    height: float
    weight: float


# Load patient data
def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data


# Save patient data
def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f, indent=4)


@app.get("/")
def hello():
    return {'message': 'Patient Management System API'}


@app.get('/about')
def about():
    return {
        'message': 'A fully functional API to manage your patient records'
    }


# View all patients
@app.get('/view')
def view():
    data = load_data()
    return data


# Create a new patient
@app.post('/create')
def createPatient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(
            status_code=400,
            detail="Patient already exists"
        )

    data[patient.id] = patient.model_dump(exclude=['id'])

    save_data(data)

    return JSONResponse(
        status_code=201,
        content={'message': 'Patient created successfully'}
    )
