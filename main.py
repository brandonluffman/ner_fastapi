# from fastapi import FastAPI
# # from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.cors import CORSMiddleware
# import spacy
# from pydantic import BaseModel
# import boto3
# import os
# import shutil


# app = FastAPI()

# def download_model_from_s3():
#     s3 = boto3.client('s3')
#     bucket_name = 'ner-model'
#     model_key = 'output/model-last'
#     local_directory = './output'

#     # Create the local directory if it doe,sn't exist
#     os.makedirs(local_directory, exist_ok=True)

#     # Download the model files from S3
#     for obj in s3.list_objects_v2(Bucket=bucket_name, Prefix=model_key)['Contents']:
#         key = obj['Key']
#         file_name = os.path.join(local_directory, key.replace(model_key, '').lstrip('/'))
#         os.makedirs(os.path.dirname(file_name), exist_ok=True)
#         s3.download_file(bucket_name, key, file_name)


# s3 = boto3.client('s3', aws_access_key_id='AKIA6QR4X5D5UUHWU264', aws_secret_access_key='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')
# nlp = spacy.load('./output/model-last')


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# class TextInput(BaseModel):
#     text: str

# class Entity(BaseModel):
#     text: str
#     start: int
#     end: int
#     label: str

# @app.post("/model")
# async def ner_model(text_input: TextInput):
#     text = text_input.text
#     doc = nlp(text)

#     entities = []
#     for entity in doc.ents:
#         entities.append(Entity(text=entity.text, start=entity.start_char, end=entity.end_char, label=entity.label_))

#     return entities, text
    

import os
import spacy
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import boto3

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

# Download the spaCy model from the S3 bucket
def download_model_from_s3():
    s3 = boto3.client('s3')
    bucket_name = 'ner-model'
    model_key = 'output/model-last'
    local_directory = './output'

    # Create the local directory if it doesn't exist
    os.makedirs(local_directory, exist_ok=True)

    # Download the model files from S3
    for obj in s3.list_objects_v2(Bucket=bucket_name, Prefix=model_key)['Contents']:
        key = obj['Key']
        file_name = os.path.join(local_directory, key.replace(model_key, '').lstrip('/'))
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        s3.download_file(bucket_name, key, file_name)

# Download the model during initialization
download_model_from_s3()

# Load the spaCy model from the local directory
nlp = spacy.load('./output/model-last')

# Define the API route
@app.post("/model")
async def ner_model(text_input: TextInput):
    text = text_input.text
    doc = nlp(text)

    entities = []
    for entity in doc.ents:
        entities.append(Entity(text=entity.text, start=entity.start_char, end=entity.end_char, label=entity.label_))

    return entities, text
