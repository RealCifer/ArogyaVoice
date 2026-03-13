import ollama
import json
import re
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

Return ONLY JSON. No explanations.
"""


def extract_json(text):
    """
    Extract JSON object from LLM output
    """

    try:
        match = re.search(r'\{[\s\S]*?\}', text)
        if match:
            return json.loads(match.group())
    except:
        pass

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
            options={"temperature": 0}
        )

        message = response["message"]["content"]

        logger.info(f"Raw LLM response: {message}")

        data = extract_json(message)

        if data:

            tool_name = data.get("tool")
            args = data.get("arguments", {})

            if tool_name:

                args["patient_id"] = patient_id

                logger.info(f"Executing tool: {tool_name}")

                return execute_tool(tool_name, **args)

        return {"message": message.strip()}

    except Exception as e:

        logger.error(f"Agent failure: {str(e)}")

        return {
            "error": "agent_error",
            "message": "The assistant encountered an error processing the request."
        }