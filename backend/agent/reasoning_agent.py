import ollama
import json
from backend.agent.tools import execute_tool
from backend.utils.logger import logger


SYSTEM_PROMPT = """
You are ArogyaVoice, an AI healthcare assistant.

You have these tools:

1. book_appointment(patient_id, doctor, time)
2. cancel_appointment(patient_id)
3. reschedule_appointment(patient_id, time)

If the user requests booking, cancelling, or rescheduling,
respond ONLY with JSON in this format:

{
 "tool": "tool_name",
 "arguments": {
   "doctor": "Doctor Name",
   "time": "HH:MM"
 }
}

Return ONLY JSON.
"""


def extract_first_json(text: str):
    """
    Extract the first valid JSON object even if the LLM adds text around it.
    Handles nested braces.
    """
    start = text.find("{")
    if start == -1:
        return None

    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[start:i+1])
                except Exception:
                    return None
    return None


def run_agent(user_text, patient_id):

    logger.info(f"Running AI agent for patient {patient_id}")

    try:

        response = ollama.chat(
            model="phi3",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            options={
                "temperature": 0
            }
        )

        message = response["message"]["content"]

        logger.info(f"Raw LLM output: {message}")

        # If the model returned quoted JSON
        if message.startswith('"') and message.endswith('"'):
            message = message[1:-1]

        data = extract_first_json(message)

        if data and "tool" in data:

            tool_name = data["tool"]
            args = data.get("arguments", {})

            args["patient_id"] = patient_id

            logger.info(f"Executing tool {tool_name} with args {args}")

            return execute_tool(tool_name, **args)

        return {"message": message.strip()}

    except Exception as e:

        logger.error(f"Agent failure: {str(e)}")

        return {
            "error": "agent_error",
            "message": "The assistant encountered an error processing the request."
        }