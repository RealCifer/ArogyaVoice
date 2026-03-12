from fastapi import FastAPI
from pydantic import BaseModel
import time

from backend.utils.language_detection import detect_language
from backend.utils.latency_logger import measure_latency
from backend.agent.reasoning_agent import run_agent

app = FastAPI(title="ArogyaVoice")

class VoiceInput(BaseModel):
    patient_id: str
    text: str


@app.get("/")
def home():
    return {"message": "ArogyaVoice API running"}


@app.post("/voice")
def voice_agent(input: VoiceInput):

    start_time = time.time()

    language = detect_language(input.text)

    ai_response = run_agent(input.text)

    latency = measure_latency(start_time)

    return {
        "language": language,
        "response": ai_response,
        "latency_ms": latency
    }