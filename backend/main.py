from fastapi import FastAPI
from pydantic import BaseModel
import time

from backend.utils.language_detection import detect_language
from backend.utils.latency_logger import measure_latency
from backend.agent.reasoning_agent import run_agent
from backend.campaigns.outbound_campaign import run_reminder_campaign
from backend.utils.performance_logger import LatencyTracker
from backend.utils.logger import logger

app = FastAPI(title="ArogyaVoice")


class VoiceInput(BaseModel):
    patient_id: str
    text: str


@app.get("/")
def home():
    return {"message": "ArogyaVoice API running"}


@app.post("/voice")
def voice_agent(input: VoiceInput):

    tracker = LatencyTracker()

    logger.info(f"Incoming request from patient {input.patient_id}")

    language = detect_language(input.text)

    ai_response = run_agent(input.text, input.patient_id)

    latency = tracker.stop()

    logger.info(f"Response generated in {latency} ms")

    return {
        "language": language,
        "response": ai_response,
        "latency_ms": latency
    }

@app.get("/campaign/reminders")
def run_campaign():

    results = run_reminder_campaign()

    return {
        "campaign": "appointment_reminders",
        "results": results
    }

@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": "ArogyaVoice",
        "version": "1.0"
    }