from datetime import date, timedelta


def calculate_next_review(score: float) -> str:
    today = date.today()

    if score >= 1.0:
        review_date = today + timedelta(days=3)

    elif score >= 0.5:
        review_date = today + timedelta(days=1)

    else:
        review_date = today

    return review_date.isoformat()