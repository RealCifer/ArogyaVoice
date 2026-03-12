import ollama

def run_agent(user_text: str):

    system_prompt = """
    You are ArogyaVoice, a healthcare voice AI assistant.

    Your job:
    - help book doctor appointments
    - help cancel appointments
    - help reschedule appointments
    """

    try:
        response = ollama.chat(
            model="phi3",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ]
        )

        return response["message"]["content"]

    except Exception as e:
        return f"AI error: {str(e)}"