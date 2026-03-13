from backend.scheduling.appointment_manager import (
    book_appointment,
    cancel_appointment,
    reschedule_appointment
)

from backend.utils.logger import logger


TOOLS = {
    "book_appointment": book_appointment,
    "cancel_appointment": cancel_appointment,
    "reschedule_appointment": reschedule_appointment
}


def execute_tool(tool_name, **kwargs):

    logger.info(f"Tool execution requested: {tool_name}")

    if tool_name not in TOOLS:
        logger.error(f"Unknown tool requested: {tool_name}")
        return {"error": "unknown_tool", "message": f"{tool_name} is not supported"}

    try:
        result = TOOLS[tool_name](**kwargs)
        logger.info(f"Tool {tool_name} executed successfully")
        return result

    except Exception as e:
        logger.error(f"Tool execution failed: {str(e)}")
        return {
            "error": "tool_execution_failed",
            "message": str(e)
        }