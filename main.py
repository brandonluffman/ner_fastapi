from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
import spacy
from pydantic import BaseModel



app = FastAPI()
# nlp = spacy.load('./output/model-last')

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

@app.post("/model")
async def ner_model(text_input: TextInput):
    text = text_input.text
    # doc = nlp(text)

    # entities = []
    # for entity in doc.ents:
    #     entities.append(Entity(text=entity.text, start=entity.start_char, end=entity.end_char, label=entity.label_))

    # return entities, text
    
    return text