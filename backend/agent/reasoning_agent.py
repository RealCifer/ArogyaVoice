import ollama
from backend.scheduling.appointment_manager import book_appointment


def run_agent(user_text, patient_id):

    text = user_text.lower()

    extraction_prompt = f"""
    Extract doctor name and appointment time from this message.

    Message: {user_text}

    Respond ONLY in this JSON format:
    {{
      "doctor": "doctor name",
      "time": "time"
    }}
    """

    try:
        extraction = ollama.chat(
            model="phi3",
            messages=[
                {"role": "user", "content": extraction_prompt}
            ]
        )

        content = extraction["message"]["content"]

        if "doctor" in content and "time" in content:
            doctor = content.split("doctor")[1].split('"')[2]
            time = content.split("time")[1].split('"')[2]

            return book_appointment(patient_id, doctor, time)

    except:
        pass

    response = ollama.chat(
        model="phi3",
        messages=[
            {"role": "system", "content": "You are ArogyaVoice, a healthcare assistant."},
            {"role": "user", "content": user_text}
        ]
    )

    return {"message": response["message"]["content"]}