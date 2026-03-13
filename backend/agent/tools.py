from backend.scheduling.appointment_manager import (
    book_appointment,
    cancel_appointment,
    reschedule_appointment
)


def execute_tool(action, patient_id, doctor=None, time=None):

    """
    Tool router used by the AI agent
    """

    if action == "book":
        return book_appointment(patient_id, doctor, time)

    if action == "cancel":
        return cancel_appointment(patient_id)

    if action == "reschedule":
        return reschedule_appointment(patient_id, time)

    return {"error": "Unknown tool action"}