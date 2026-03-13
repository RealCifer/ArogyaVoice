import ollama
import json
from backend.agent.tools import execute_tool
from backend.utils.logger import logger


SYSTEM_PROMPT = """
You are ArogyaVoice, an AI healthcare assistant for booking clinical appointments.

Available tools:

1. book_appointment(patient_id, doctor, time)
2. cancel_appointment(patient_id)
3. reschedule_appointment(patient_id, time)

Rules:
- If the user wants to book, cancel, or reschedule an appointment,
  respond ONLY with JSON in the format:

{
  "tool": "tool_name",
  "arguments": {
      "doctor": "Doctor Name",
      "time": "HH:MM"
  }
}

Example:

User: Book appointment with Dr Mehta at 4pm

Response:
{
 "tool": "book_appointment",
 "arguments": {
   "doctor": "Dr Mehta",
   "time": "16:00"
 }
}

If the request does not require a tool, respond with normal conversational text.
"""


def run_agent(user_text, patient_id):

    logger.info(f"Running AI agent for patient {patient_id}")

    try:

        response = ollama.chat(
            model="phi3",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ]
        )

        message = response["message"]["content"].strip()

        logger.info(f"LLM response: {message}")

        try:

            data = json.loads(message)

            tool_name = data.get("tool")
            args = data.get("arguments", {})

            if tool_name:

                args["patient_id"] = patient_id

                logger.info(f"Executing tool: {tool_name} with args {args}")

                result = execute_tool(tool_name, **args)

                return result

        except json.JSONDecodeError:
            # LLM returned normal text
            logger.info("LLM returned conversational response")
            return {"message": message}

        return {"message": message}

    except Exception as e:

        logger.error(f"Agent failure: {str(e)}")

        return {
            "error": "agent_error",
            "message": "The assistant encountered an error processing the request."
        }