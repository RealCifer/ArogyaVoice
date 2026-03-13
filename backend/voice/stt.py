import whisper

model = whisper.load_model("base")


def speech_to_text(audio_path: str):

    """
    Converts speech audio to text
    """

    result = model.transcribe(audio_path)

    return result["text"]