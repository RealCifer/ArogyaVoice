from gtts import gTTS
import os


def text_to_speech(text, output_file="response.mp3"):

    """
    Convert text response to speech
    """

    tts = gTTS(text=text)

    tts.save(output_file)

    return output_file