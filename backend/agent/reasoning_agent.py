import ollama
import json
from backend.agent.tools import execute_tool


SYSTEM_PROMPT = """
You are ArogyaVoice, an AI healthcare assistant.

Available tools:

1. book_appointment(patient_id, doctor, time)
2. cancel_appointment(patient_id)
3. reschedule_appointment(patient_id, time)

If the user asks for scheduling actions,
respond ONLY with JSON:

{
 "tool": "tool_name",
 "arguments": {...}
}

If no tool is required, respond normally.
"""


def run_agent(user_text, patient_id):

    response = ollama.chat(
        model="phi3",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ]
    )

    message = response["message"]["content"]

    try:
        data = json.loads(message)

        tool = data["tool"]
        args = data["arguments"]

        args["patient_id"] = patient_id

        return execute_tool(tool, **args)

    except:
        return {"message": message}