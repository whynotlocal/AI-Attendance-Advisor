# ============================================================
# AI ATTENDANCE ADVISOR
# ============================================================

REQUIRED_ATTENDANCE = 75


def calculate_required_classes(present, total):
    """
    Calculate how many consecutive classes
    a student needs to attend to reach 75%.
    """

    if total == 0:
        return 0

    current_percentage = (present / total) * 100

    if current_percentage >= REQUIRED_ATTENDANCE:
        return 0

    required = 0

    # Formula:
    # (present + x) / (total + x) >= 0.75

    while ((present + required) / (total + required)) * 100 < REQUIRED_ATTENDANCE:
        required += 1

    return required


def predict_eligibility(present, total):
    """
    Determine attendance percentage,
    eligibility, risk and recommendation.
    """

    if total == 0:

        return {
            "percentage": 0,
            "status": "Not Eligible",
            "risk": "High",
            "required_classes": 0,
            "message": "No attendance data available."
        }


    percentage = (present / total) * 100


    # --------------------------------------------------------
    # Determine risk
    # --------------------------------------------------------

    if percentage >= 85:

        risk = "Low"

    elif percentage >= 75:

        risk = "Medium"

    elif percentage >= 65:

        risk = "High"

    else:

        risk = "Very High"


    # --------------------------------------------------------
    # Eligibility
    # --------------------------------------------------------

    if percentage >= REQUIRED_ATTENDANCE:

        status = "Eligible"

        required_classes = 0

    else:

        status = "Not Eligible"

        required_classes = calculate_required_classes(
            present,
            total
        )


    # --------------------------------------------------------
    # Advisor recommendation
    # --------------------------------------------------------

    if percentage >= 85:

        message = (
            "Excellent attendance. "
            "You are safely above the minimum requirement. "
            "Continue maintaining your attendance."
        )

    elif percentage >= 75:

        message = (
            "Your attendance currently meets the minimum "
            "eligibility requirement. However, maintain "
            "regular attendance to avoid falling below 75%."
        )

    elif percentage >= 65:

        message = (
            "Warning: Your attendance is below the required "
            "75%. Attend upcoming classes regularly to improve "
            "your eligibility."
        )

    else:

        message = (
            "Critical attendance warning. Your attendance is "
            "significantly below the required 75%. You should "
            "attend upcoming classes consistently and contact "
            "your academic advisor if necessary."
        )


    return {
        "percentage": percentage,
        "status": status,
        "risk": risk,
        "required_classes": required_classes,
        "message": message
    }