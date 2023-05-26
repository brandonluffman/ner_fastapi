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

# def load_model_from_s3(bucket_name, model_key, aws_access_key_id, aws_secret_access_key, region_name):
#     s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
#     response = s3.get_object(Bucket=bucket_name, Key=model_key)
#     model_bytes = response['Body'].read()

#     with tempfile.NamedTemporaryFile() as temp_file:
#         temp_file.write(model_bytes)
#         temp_file.flush()
#         model = spacy.load(temp_file.name)
    
#     return model

# # Set up the AWS credentials
# aws_access_key_id = 'AKIA6QR4X5D5UUHWU264'
# aws_secret_access_key = 'dC//cBLCMRreENi6vfVAVS5EId15TP5pJwMsuqCF'
# bucket_name = 'ner-model'
# model_key = 'output/model-last'
# region_name = 'us-east-1'  # Replace with your bucket's region


# # Load the spaCy model from the S3 bucket
# nlp = load_model_from_s3(bucket_name, model_key, aws_access_key_id, aws_secret_access_key, region_name)

# Define the API route
@app.post("/model")
async def ner_model(text_input: TextInput):
    text = text_input.text
    # doc = nlp(text)

    # entities = []
    # for entity in doc.ents:
    #     entities.append(Entity(text=entity.text, start=entity.start_char, end=entity.end_char, label=entity.label_))

    # return entities, text
    return text