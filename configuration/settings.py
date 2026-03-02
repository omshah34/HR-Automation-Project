# ==================================================
# SETTINGS
# ==================================================

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "llama-3.3-70b-versatile"

# Must match your Google Sheet name exactly
SHEET_NAME = "Job Recruitment form (Responses)"

# Poll interval in seconds
POLL_INTERVAL = 30