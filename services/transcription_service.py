import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def transcribe_audio(uploaded_file):
    """Convert an uploaded audio recording into text."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing.")

    client = Groq(api_key=api_key)

    transcription = client.audio.transcriptions.create(
        file=(uploaded_file.name, uploaded_file.getvalue()),
        model="whisper-large-v3-turbo",
        response_format="json",
    )

    return transcription.text
