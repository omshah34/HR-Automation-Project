# ==================================================
# MAIN ENTRY POINT
# ==================================================

import time
import logging

from configuration.settings import POLL_INTERVAL
from configuration.job_descriptions import JOB_DESCRIPTIONS

from services.sheet_service import get_all_rows, update_candidate_row
from services.resume_service import extract_resume_text
from services.scoring_service import score_candidate
from services.decision_service import decide


# ==================================================
# LOGGING CONFIGURATION
# ==================================================

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==================================================
# MAIN PROCESSING FUNCTION
# ==================================================

def process_candidates():

    print("🚀 HR Automation Started")

    while True:

        try:
            print("\n🔎 Checking for new candidates...")
            rows = get_all_rows()

            for index, row in enumerate(rows):

                # Sheet header is row 1 → data starts at row 2
                sheet_row_number = index + 2

                processed = str(row.get("processed", "")).strip().lower()

                if processed == "true":
                    continue

                name = row.get("Full Name")
                job_role = row.get("Job Role Selection(Apply for which role?)")
                resume_link = row.get("Upload Your Resume")

                print(f"\n➡ Processing: {name} | {job_role}")

                # --------------------------------------------------
                # Validate Job Role
                # --------------------------------------------------

                job_description = JOB_DESCRIPTIONS.get(job_role)

                if not job_description:
                    print("❌ Invalid job role. Skipping.")
                    continue

                # --------------------------------------------------
                # Extract Resume
                # --------------------------------------------------

                resume_text = extract_resume_text(resume_link)

                if not resume_text:
                    print("❌ Resume extraction failed.")
                    update_candidate_row(sheet_row_number, 0, "failed", True)
                    continue

                print("📄 Resume extracted")

                # --------------------------------------------------
                # AI Scoring
                # --------------------------------------------------

                score_result = score_candidate(
                    job_role=job_role,
                    job_description=job_description,
                    resume_text=resume_text
                )

                total_score = score_result.get("total_score", 0)

                print(f"🧠 Score: {total_score}")

                # --------------------------------------------------
                # Decision
                # --------------------------------------------------

                decision = decide(total_score)

                print(f"✅ Decision: {decision}")

                # --------------------------------------------------
                # Reason
                # --------------------------------------------------

                reason = score_result.get("reason", "No reason provided")

                # --------------------------------------------------
                # Update Sheet
                # --------------------------------------------------

                update_candidate_row(
                    row_number=sheet_row_number,
                    total_score=total_score,
                    decision=decision,
                    reason=reason,
                    processed=True
                )   

                print("📊 Sheet updated")
                logging.info(f"{name} | {job_role} | {total_score} | {decision}")

        except Exception as e:
            print(f"🔥 Unexpected Error: {e}")
            logging.error(str(e))

        print(f"\n⏳ Sleeping {POLL_INTERVAL} seconds...")
        time.sleep(POLL_INTERVAL)


# ==================================================
# SCRIPT START
# ==================================================

if __name__ == "__main__":
    process_candidates()