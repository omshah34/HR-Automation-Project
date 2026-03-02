# ==================================================
# SCORING SERVICE
# ==================================================

import json
from groq import Groq
from configuration.settings import GROQ_API_KEY, MODEL_NAME


# Initialize Groq client once
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

client = Groq(api_key=GROQ_API_KEY)


# ==================================================
# BUILD PROMPT
# ==================================================

def build_prompt(job_role: str, job_description: str, resume_text: str) -> str:
    """
    Build structured scoring prompt.
    """

    return f"""
You are an HR AI scoring engine.

Job Role:
{job_role}

Job Description:
{job_description}

Candidate Resume:
{resume_text}

Score strictly based on job match.

Return JSON only in this exact format:
{{
  "skill_match": number (0-50),
  "experience_match": number (0-30),
  "project_relevance": number (0-20),
  "total_score": number,
  "reason": "max 2 lines explanation"
}}

Do not return anything except JSON.
"""


# ==================================================
# SAFE JSON PARSER
# ==================================================

def safe_json_parse(response_text: str) -> dict:
    """
    Safely extract JSON from model response.
    """

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        start = response_text.find("{")
        end = response_text.rfind("}") + 1

        if start != -1 and end != -1:
            try:
                return json.loads(response_text[start:end])
            except json.JSONDecodeError:
                return {}

    return {}


# ==================================================
# MAIN SCORING FUNCTION
# ==================================================

def score_candidate(job_role: str,
                    job_description: str,
                    resume_text: str) -> dict:
    """
    Call Groq API and return structured score.
    """

    prompt = build_prompt(job_role, job_description, resume_text)

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()

        result = safe_json_parse(content)

        if "total_score" not in result:
            return {
                "total_score": 0,
                "reason": "Invalid AI response"
            }

        return result

    except Exception as e:
        return {
            "total_score": 0,
            "reason": f"Scoring failed: {str(e)}"
        }