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


# Set up the AWS credentials
aws_access_key_id = 'AKIA6QR4X5D5UUHWU264'
aws_secret_access_key = 'dC//cBLCMRreENi6vfVAVS5EId15TP5pJwMsuqCF'
bucket_name = 'ner-model'
model_key = 'model.tar.gz'
region_name = 'us-east-1'  # Replace with your bucket's region


def load_model_from_s3(bucket_name, model_key):
    # Create a session using your AWS credentials
    session = boto3.Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # Create an S3 client using the session
    s3_client = session.client('s3')

    # Download the model file from S3
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=model_key)
        model_data = response['Body'].read()
    except:
        return None  # Return None or handle the error as per your requirement

    # Load the model using spaCy from the in-memory buffer
    model_buffer = BytesIO(model_data)
    nlp = spacy.load(model_buffer)

    return nlp


class TextInput(BaseModel):
    text: str


# Define the API route
@app.post("/model")
async def ner_model(text_input: TextInput):
    text = text_input.text

    nlp = load_model_from_s3(bucket_name, model_key)

    if nlp is None:
        return {'message': 'Failed to load model'}

    # Perform any further operations with the loaded model
    # For example, you can process the provided text using the model
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    return {'message': 'Model loaded successfully', 'entities': entities}