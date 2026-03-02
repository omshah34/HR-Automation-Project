# ==================================================
# RESUME SERVICE
# ==================================================

import os
import re
import requests
import pdfplumber


# ==================================================
# EXTRACT DRIVE FILE ID
# ==================================================

def extract_drive_file_id(drive_link: str) -> str:
    """
    Extract file ID from multiple Google Drive link formats.
    """

    if not drive_link:
        return None

    patterns = [
        r"/d/([a-zA-Z0-9_-]+)",
        r"id=([a-zA-Z0-9_-]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, drive_link)
        if match:
            return match.group(1)

    return None


# ==================================================
# DOWNLOAD RESUME
# ==================================================

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials
import io


def download_resume(drive_link: str) -> str:

    file_id = extract_drive_file_id(drive_link)

    if not file_id:
        print("❌ File ID extraction failed")
        return None

    # Authenticate with service account
    scopes = ["https://www.googleapis.com/auth/drive.readonly"]

    credentials = Credentials.from_service_account_file(
        "service_account.json",
        scopes=scopes
    )

    drive_service = build("drive", "v3", credentials=credentials)

    request = drive_service.files().get_media(fileId=file_id)

    file_stream = io.BytesIO()
    downloader = MediaIoBaseDownload(file_stream, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()

    os.makedirs("temp", exist_ok=True)
    file_path = f"temp/{file_id}.pdf"

    with open(file_path, "wb") as f:
        f.write(file_stream.getvalue())

    return file_path


# ==================================================
# EXTRACT TEXT FROM PDF
# ==================================================

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from PDF file.
    """

    if not file_path or not os.path.exists(file_path):
        return None

    text = ""

    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception:
        return None

    return text.strip()


# ==================================================
# MAIN FUNCTION USED BY MAIN.PY
# ==================================================

def extract_resume_text(drive_link: str) -> str:
    """
    Complete flow:
    1. Download resume
    2. Extract text
    3. Return extracted text
    """

    file_path = download_resume(drive_link)

    if not file_path:
        return None

    resume_text = extract_text_from_pdf(file_path)

    return resume_text