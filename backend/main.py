from fastapi import FastAPI
from pydantic import BaseModel

from backend.utils.language_detection import detect_language
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

    try:

        logger.info(f"Incoming request from patient {input.patient_id}")

        # Detect language
        language = detect_language(input.text)

        # Run AI reasoning agent
        ai_response = run_agent(input.text, input.patient_id)

        # Measure latency
        latency = tracker.stop()

        logger.info(f"Response generated in {latency} ms")

        return {
            "agent": "phi3_local_llm",
            "language": language,
            "response": ai_response,
            "latency_ms": latency
        }

    except Exception as e:

        logger.error(f"API error: {str(e)}")

        return {
            "error": "server_error",
            "message": "An error occurred while processing the request"
        }


@app.get("/campaign/reminders")
def run_campaign():

    logger.info("Running reminder campaign")

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