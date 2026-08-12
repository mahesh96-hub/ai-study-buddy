from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


INDIA_TIMEZONE = ZoneInfo("Asia/Kolkata")


def calculate_next_review(score: float) -> str:
    today = datetime.now(INDIA_TIMEZONE).date()

    if score >= 1.0:
        review_date = today + timedelta(days=3)

    elif score >= 0.5:
        review_date = today + timedelta(days=1)

    else:
        review_date = today

    return review_date.isoformat()