import os
import boto3
import spacy
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from io import BytesIO, StringIO
import tempfile


# Initialize FastAPI
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextInput(BaseModel):
    text: str

class Entity(BaseModel):
    text: str
    start: int
    end: int
    label: str


class TextInput(BaseModel):
    text: str


# Define the API route
@app.post("/model")
async def ner_model(text_input: TextInput):
    text = text_input.text

    return text