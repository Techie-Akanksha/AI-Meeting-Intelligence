
import os
import tempfile

from moviepy import VideoFileClip


def extract_audio_from_video(uploaded_video):
    """
    Extract audio from an uploaded video.

    Returns the path to a temporary WAV audio file.
    """

    video_path = None
    audio_path = None

    try:
        # Create a temporary video file
        suffix = os.path.splitext(uploaded_video.name)[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_video:
            temp_video.write(uploaded_video.getvalue())
            video_path = temp_video.name

        # Create a temporary output audio path
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as temp_audio:
            audio_path = temp_audio.name

        # Open video and extract its audio
        with VideoFileClip(video_path) as video:

            if video.audio is None:
                raise ValueError(
                    "The uploaded video has no audio track."
                )

            video.audio.write_audiofile(
                audio_path,
                codec="pcm_s16le",
                fps=16000,
                nbytes=2,
                logger=None
            )

        return audio_path

    except Exception:
        # Remove incomplete audio file if extraction fails
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)

        raise

    finally:
        # Always remove the temporary video file
        if video_path and os.path.exists(video_path):
            os.remove(video_path)
