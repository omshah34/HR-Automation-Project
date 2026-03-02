# ==================================================
# SHEET SERVICE
# ==================================================

import gspread
from google.oauth2.service_account import Credentials
from configuration.settings import SHEET_NAME


# ==================================================
# GOOGLE SHEET CONNECTION
# ==================================================

def get_sheet():
    """
    Authenticate and return Google Sheet object.
    """

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    credentials = Credentials.from_service_account_file(
        "service_account.json",
        scopes=scope
    )

    client = gspread.authorize(credentials)

    return client.open(SHEET_NAME).sheet1


# ==================================================
# FETCH ALL ROWS
# ==================================================

def get_all_rows():
    """
    Fetch all rows from sheet as list of dictionaries.
    """

    sheet = get_sheet()
    return sheet.get_all_records()


# ==================================================
# UPDATE CANDIDATE ROW
# ==================================================

def update_candidate_row(row_number: int,
                         total_score: int,
                         decision: str,
                         reason: str,
                         processed: bool):

    sheet = get_sheet()
    headers = sheet.row_values(1)

    try:
        score_col = headers.index("total_score") + 1
        decision_col = headers.index("decision") + 1
        reason_col = headers.index("reason") + 1
        processed_col = headers.index("processed") + 1
    except ValueError:
        raise Exception(
            "Required columns missing. Add: total_score, decision, reason, processed"
        )

    sheet.update_cell(row_number, score_col, total_score)
    sheet.update_cell(row_number, decision_col, decision)
    sheet.update_cell(row_number, reason_col, reason)
    sheet.update_cell(row_number, processed_col, str(processed))