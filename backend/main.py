from fastapi import FastAPI
from pydantic import BaseModel
import time

app = FastAPI(title="ArogyaVoice")

class VoiceInput(BaseModel):
    patient_id: str
    text: str


@app.get("/")
def home():
    return {"message": "ArogyaVoice API running"}


@app.post("/voice")
def voice_agent(input: VoiceInput):

    start = time.time()

    response = "How can I help you with your appointment?"

    latency = (time.time() - start) * 1000

    return {
        "language": "English",
        "response": response,
        "latency_ms": round(latency,2)
    }