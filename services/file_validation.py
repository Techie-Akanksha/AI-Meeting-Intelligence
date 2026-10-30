
MAX_MEDIA_SIZE_MB = 25

def validate_media_file(uploaded_file):
    """
    Check whether an uploaded media file
    is within the allowed size limit.
    """

    if uploaded_file is None:
        raise ValueError("No file was uploaded.")

    file_size_mb = uploaded_file.size / (1024 * 1024)

    if file_size_mb > MAX_MEDIA_SIZE_MB:
        raise ValueError(
            f"File is too large ({file_size_mb:.2f} MB). "
            f"Maximum allowed size is {MAX_MEDIA_SIZE_MB} MB."
        )

    return True
