import os
import re


def is_supported_file(filename: str) -> bool:
    """
    Check if the file has a supported extension (PDF or DOCX).
    """
    supported_extensions = {".pdf", ".docx"}
    _, ext = os.path.splitext(filename.lower())
    return ext in supported_extensions


def clean_text(text: str) -> str:
    """
    Basic text cleaning: normalize whitespace and strip leading/trailing spaces.
    """
    if not text:
        return text
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def save_uploaded_file(uploaded_file, tmp_dir="/tmp") -> str:
    """
    Save a Streamlit uploaded file to a temporary local path.

    Returns the filepath.
    """
    import tempfile

    suffix = os.path.splitext(uploaded_file.name)[1] if hasattr(uploaded_file, 'name') else ""
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir=tmp_dir) as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name
    return temp_path


def delete_file_safely(filepath: str):
    """
    Attempt to delete a file, ignoring errors.
    """
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception:
        pass
