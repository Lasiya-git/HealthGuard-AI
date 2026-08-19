from src.knowledge_base import load_health_data


def analyze_risk(question):
    """
    Analyze the user's question for known warning signs.
    """

    data = load_health_data()

    question = question.lower()

    detected_warning_signs = []
    related_conditions = []

    # Check every condition in the knowledge base
    for information in data.values():

        for warning_sign in information["warning_signs"]:

            warning = warning_sign.lower()

            if warning in question:
                detected_warning_signs.append(warning_sign)

                if information["name"] not in related_conditions:
                    related_conditions.append(
                        information["name"]
                    )

    # Remove duplicate warning signs
    detected_warning_signs = list(
        dict.fromkeys(detected_warning_signs)
    )

    # Determine guidance level
    if detected_warning_signs:

        level = "URGENT ATTENTION"

        message = (
            "Some warning signs were detected in your message. "
            "This does not confirm a diagnosis. "
            "Consider seeking prompt professional medical evaluation."
        )

    else:

        level = "GENERAL AWARENESS"

        message = (
            "No specific warning signs from the current "
            "knowledge base were detected. Continue monitoring "
            "your symptoms and seek professional advice if they "
            "become severe or worsen."
        )

    return {
        "level": level,
        "warning_signs": detected_warning_signs,
        "related_conditions": related_conditions,
        "message": message
    }