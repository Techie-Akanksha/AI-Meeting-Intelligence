
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def transcribe_audio(audio_source):
    """
    Transcribe an uploaded audio file or a local audio path.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing.")

    client = Groq(api_key=api_key)

    if isinstance(audio_source, str):
        # Audio extracted from video
        with open(audio_source, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3-turbo",
                response_format="json"
            )

    else:
        # Audio uploaded directly through Streamlit
        transcription = client.audio.transcriptions.create(
            file=(
                audio_source.name,
                audio_source.getvalue()
            ),
            model="whisper-large-v3-turbo",
            response_format="json"
        )

    return transcription.text
