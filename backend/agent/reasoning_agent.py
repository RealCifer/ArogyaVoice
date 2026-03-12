import ollama

def run_agent(user_text):

    system_prompt = """
    You are ArogyaVoice, a healthcare voice AI assistant.

    You help patients:
    - book appointments
    - cancel appointments
    - reschedule appointments

    Be polite and clear.
    """

    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ]
    )

    return response["message"]["content"]