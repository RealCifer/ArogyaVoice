from backend.scheduling.appointment_manager import appointments
from backend.agent.reasoning_agent import run_agent


def run_reminder_campaign():

    reminders = []

    for appt in appointments:

        patient_id = appt["patient_id"]
        doctor = appt["doctor"]
        time = appt["time"]

        message = f"Reminder: You have an appointment with {doctor} at {time}. Would you like to confirm or reschedule?"

        ai_response = run_agent(message, patient_id)

        reminders.append({
            "patient_id": patient_id,
            "message_sent": message,
            "agent_response": ai_response
        })

    return reminders