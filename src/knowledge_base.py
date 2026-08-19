import json
import os


# Find the project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to health database
DATA_FILE = os.path.join(BASE_DIR, "data", "health_data.json")


def load_health_data():
    """Load health information from the JSON database."""

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def search_disease(disease_name):
    """Search for a disease by name."""

    data = load_health_data()

    disease_name = disease_name.lower().strip()

    for key, information in data.items():

        if key.lower() == disease_name:
            return information

    return None


def search_symptom(symptom):
    """Find diseases associated with a symptom."""

    data = load_health_data()

    symptom = symptom.lower().strip()

    results = []

    for information in data.values():

        symptoms = [
            item.lower()
            for item in information["common_symptoms"]
        ]

        if symptom in symptoms:
            results.append(information)

    return results