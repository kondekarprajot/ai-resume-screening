from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile


def save_uploaded_file(uploaded_file, upload_dir: str | Path) -> Path:
    """Persist a Streamlit uploaded file and return its path."""
    directory = Path(upload_dir)
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / uploaded_file.name
    destination.write_bytes(uploaded_file.getbuffer())
    return destination


def save_temp_upload(uploaded_file) -> Path:
    """Save an uploaded file to a temporary path for parsing."""
    suffix = Path(uploaded_file.name).suffix
    with NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        return Path(temp_file.name)


def comma_join(values: list[str]) -> str:
    return ", ".join(values) if values else "-"
