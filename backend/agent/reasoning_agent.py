import ollama
from backend.scheduling.appointment_manager import book_appointment, cancel_appointment, reschedule_appointment


def run_agent(user_text, patient_id):

    text = user_text.lower()

    if "book" in text:
        return book_appointment(patient_id, "Dr Sharma", "10:00 AM")

    if "cancel" in text:
        return cancel_appointment(patient_id)

    if "reschedule" in text:
        return reschedule_appointment(patient_id, "4:00 PM")

    response = ollama.chat(
        model="phi3",
        messages=[
            {"role": "system", "content": "You are ArogyaVoice, a healthcare assistant."},
            {"role": "user", "content": user_text}
        ]
    )

    return {"message": response["message"]["content"]}