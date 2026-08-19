from src.knowledge_base import load_health_data


def detect_intent(question):
    """
    Detect the main intention of the user's question.
    """

    question = question.lower().strip()

    # Prevention
    if any(word in question for word in [
        "prevent",
        "prevention",
        "avoid",
        "protect",
        "protection",
        "how to stop"
    ]):
        return "prevention"

    # Warning signs
    if any(word in question for word in [
        "warning",
        "danger",
        "serious",
        "emergency",
        "when to worry"
    ]):
        return "warning"

    # Symptoms
    if any(word in question for word in [
        "symptom",
        "symptoms",
        "sign",
        "signs",
        "i have",
        "i feel",
        "feeling"
    ]):
        return "symptoms"

    # Description
    if any(phrase in question for phrase in [
        "what is",
        "what are",
        "tell me about",
        "explain",
        "meaning of"
    ]):
        return "description"

    return "general"


def find_direct_disease_matches(question, data):
    """
    Find diseases explicitly mentioned by the user.
    """

    question = question.lower()

    matches = []

    for key, information in data.items():

        disease_name = information["name"].lower()

        if key.lower() in question or disease_name in question:
            matches.append(information)

    return matches


def calculate_symptom_score(question, information):
    """
    Calculate how strongly the user's symptoms
    match a health topic.
    """

    question = question.lower()

    score = 0

    symptoms = [
        symptom.lower()
        for symptom in information["common_symptoms"]
    ]

    for symptom in symptoms:

        # Multi-word symptom
        if symptom in question:
            score += 3

        # Individual words
        symptom_words = symptom.split()

        for word in symptom_words:

            if len(word) >= 4 and word in question:
                score += 1

    return score


def find_symptom_matches(question, data):
    """
    Find health topics based on symptom overlap.
    """

    scored_results = []

    for information in data.values():

        score = calculate_symptom_score(
            question,
            information
        )

        if score > 0:

            scored_results.append(
                (score, information)
            )

    scored_results.sort(
        key=lambda item: item[0],
        reverse=True
    )

    if not scored_results:
        return []

    # Keep strong matches only
    highest_score = scored_results[0][0]

    results = [
        information
        for score, information in scored_results
        if score >= highest_score - 2
    ]

    return results[:3]


def find_relevant_health_info(question):
    """
    Main retrieval function.
    """

    data = load_health_data()

    intent = detect_intent(question)

    # --------------------------------------------------
    # Direct disease detection
    # --------------------------------------------------

    direct_matches = find_direct_disease_matches(
        question,
        data
    )

    if direct_matches:
        return direct_matches

    # --------------------------------------------------
    # Symptom-based matching
    # --------------------------------------------------

    if intent == "symptoms":

        return find_symptom_matches(
            question,
            data
        )

    # --------------------------------------------------
    # General keyword matching
    # --------------------------------------------------

    question_words = set(
        question.lower().split()
    )

    results = []

    for information in data.values():

        score = 0

        description = information[
            "description"
        ].lower()

        prevention = [
            item.lower()
            for item in information["prevention"]
        ]

        warnings = [
            item.lower()
            for item in information["warning_signs"]
        ]

        symptoms = [
            item.lower()
            for item in information["common_symptoms"]
        ]

        # Match prevention intent
        if intent == "prevention":

            for word in question_words:

                for item in prevention:

                    if word in item:
                        score += 3

        # Match warning intent
        elif intent == "warning":

            for word in question_words:

                for item in warnings:

                    if word in item:
                        score += 3

        # General matching
        for word in question_words:

            if len(word) >= 4:

                if word in description:
                    score += 1

                for symptom in symptoms:

                    if word in symptom:
                        score += 1

        if score > 0:

            results.append(
                (score, information)
            )

    results.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        information
        for score, information in results[:3]
    ]


def generate_basic_response(question):
    """
    Generate a structured health-awareness response.
    """

    results = find_relevant_health_info(question)

    intent = detect_intent(question)

    if not results:

        return {
            "message": (
                "I could not find enough verified information "
                "in the current HealthGuard knowledge base."
            ),
            "intent": intent,
            "results": []
        }

    response = []

    for information in results:

        response.append({
            "name": information["name"],
            "description": information["description"],
            "symptoms": information["common_symptoms"],
            "prevention": information["prevention"],
            "warning_signs": information["warning_signs"],
            "sources": information["sources"]
        })

    # --------------------------------------------------
    # Response message
    # --------------------------------------------------

    if intent == "prevention":

        message = (
            "🛡️ Here are prevention measures from "
            "the HealthGuard trusted knowledge base."
        )

    elif intent == "warning":

        message = (
            "⚠️ Here are the warning signs associated "
            "with the relevant health topic."
        )

    elif intent == "symptoms":

        if len(response) > 1:

            message = (
                "🟡 Fever and other common symptoms can "
                "overlap across different health conditions. "
                "The topics below are for awareness only "
                "and do not confirm a diagnosis."
            )

        else:

            message = (
                "🔍 Here are the symptoms listed in the "
                "HealthGuard knowledge base. Symptoms alone "
                "cannot confirm a disease."
            )

    elif intent == "description":

        message = (
            "📚 Here is trusted health-awareness "
            "information about the requested topic."
        )

    else:

        message = (
            "Here is health-awareness information "
            "related to your question."
        )

    return {
        "message": message,
        "intent": intent,
        "results": response
    }