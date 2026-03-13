from backend.scheduling.appointment_manager import (
    book_appointment,
    cancel_appointment,
    reschedule_appointment
)

TOOLS = {
    "book_appointment": book_appointment,
    "cancel_appointment": cancel_appointment,
    "reschedule_appointment": reschedule_appointment
}


def execute_tool(tool_name, **kwargs):

    if tool_name not in TOOLS:
        return {"error": "unknown tool"}

    return TOOLS[tool_name](**kwargs)