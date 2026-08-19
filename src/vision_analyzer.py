import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


# Load Gemini API key from .env
load_dotenv()


def analyze_image_awareness(uploaded_image):
    """
    Gemini-powered visual health awareness analysis.

    The system describes visible features for awareness only.
    It does not diagnose medical conditions.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    # --------------------------------------------------
    # API KEY CHECK
    # --------------------------------------------------

    if not api_key:

        return {
            "observation": (
                "The AI vision service is not configured."
            ),
            "possible_category": "AI vision unavailable",
            "confidence": "Low",
            "guidance": (
                "The visual awareness service is currently "
                "not configured."
            ),
            "recommendation": (
                "Please check the HealthGuard AI configuration."
            ),
            "disclaimer": (
                "This feature is for health awareness only "
                "and is not a medical diagnosis."
            )
        }

    try:

        # --------------------------------------------------
        # GEMINI CLIENT
        # --------------------------------------------------

        client = genai.Client(
            api_key=api_key
        )

        # --------------------------------------------------
        # SAFETY-FOCUSED PROMPT
        # --------------------------------------------------

        prompt = """
You are HealthGuard AI, a public health awareness assistant.

Analyze the uploaded image ONLY for visible features.

IMPORTANT SAFETY RULES:

1. Never diagnose a disease.
2. Never say the person definitely has a condition.
3. Describe only visible characteristics.
4. Give broad awareness categories only.
5. Do not prescribe medicines.
6. Do not recommend specific medication.
7. If the image is unclear, say so.
8. Do not identify the person.
9. Encourage professional medical evaluation when appropriate.
10. Avoid unsupported medical claims.

Return exactly these six fields:

OBSERVATION:
Briefly describe visible features.

POSSIBLE_CATEGORY:
Give a broad health-awareness category.

CONFIDENCE:
Use only Low, Moderate, or High.

GUIDANCE:
Give general health-awareness information.

RECOMMENDATION:
Give safe general next steps.

DISCLAIMER:
State that this is health awareness only and cannot
confirm a medical condition.
"""

        # --------------------------------------------------
        # IMAGE
        # --------------------------------------------------

        image_bytes = uploaded_image.getvalue()

        mime_type = uploaded_image.type

        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=mime_type
        )

        # --------------------------------------------------
        # GEMINI VISION
        # --------------------------------------------------

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[
                prompt,
                image_part
            ]
        )

        text = response.text

        # --------------------------------------------------
        # RESPONSE VARIABLES
        # --------------------------------------------------

        observation = ""
        possible_category = ""
        confidence = ""
        guidance = ""
        recommendation = ""
        disclaimer = ""

        current_section = None

        # --------------------------------------------------
        # PARSE RESPONSE
        # --------------------------------------------------

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            upper_line = line.upper()

            if upper_line.startswith("OBSERVATION:"):

                current_section = "observation"

                observation = line.split(
                    ":", 1
                )[1].strip()

            elif upper_line.startswith(
                "POSSIBLE_CATEGORY:"
            ):

                current_section = "possible_category"

                possible_category = line.split(
                    ":", 1
                )[1].strip()

            elif upper_line.startswith("CONFIDENCE:"):

                current_section = "confidence"

                confidence = line.split(
                    ":", 1
                )[1].strip()

            elif upper_line.startswith("GUIDANCE:"):

                current_section = "guidance"

                guidance = line.split(
                    ":", 1
                )[1].strip()

            elif upper_line.startswith(
                "RECOMMENDATION:"
            ):

                current_section = "recommendation"

                recommendation = line.split(
                    ":", 1
                )[1].strip()

            elif upper_line.startswith("DISCLAIMER:"):

                current_section = "disclaimer"

                disclaimer = line.split(
                    ":", 1
                )[1].strip()

            else:

                if current_section == "observation":

                    observation += " " + line

                elif current_section == "possible_category":

                    possible_category += " " + line

                elif current_section == "confidence":

                    confidence += " " + line

                elif current_section == "guidance":

                    guidance += " " + line

                elif current_section == "recommendation":

                    recommendation += " " + line

                elif current_section == "disclaimer":

                    disclaimer += " " + line

        # --------------------------------------------------
        # SAFE RESULT
        # --------------------------------------------------

        return {
            "observation": (
                observation
                or "No clear visual observation "
                   "could be generated."
            ),

            "possible_category": (
                possible_category
                or "No clear health-related observation"
            ),

            "confidence": (
                confidence
                if confidence in [
                    "Low",
                    "Moderate",
                    "High"
                ]
                else "Low"
            ),

            "guidance": (
                guidance
                or (
                    "The image should be interpreted only "
                    "as general health-awareness information."
                )
            ),

            "recommendation": (
                recommendation
                or (
                    "If the concern persists or worsens, "
                    "consider consulting a qualified "
                    "healthcare professional."
                )
            ),

            "disclaimer": (
                disclaimer
                or (
                    "This AI image analysis is for health "
                    "awareness only and cannot confirm "
                    "or rule out a medical condition."
                )
            )
        }

    # --------------------------------------------------
    # QUOTA / RATE LIMIT
    # --------------------------------------------------

    except Exception as e:

        error_text = str(e)

        # 429 = quota/rate limit
        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:

            return {
                "observation": (
                    "AI visual analysis is temporarily "
                    "unavailable because the service "
                    "has reached its current request limit."
                ),
                "possible_category": (
                    "AI vision temporarily unavailable"
                ),
                "confidence": "Low",
                "guidance": (
                    "Please wait a short while before "
                    "trying the image analysis again."
                ),
                "recommendation": (
                    "You can continue using the HealthGuard "
                    "AI health-awareness chatbot while the "
                    "vision service becomes available."
                ),
                "disclaimer": (
                    "This feature is for health awareness "
                    "only and cannot provide a medical diagnosis."
                )
            }

        # 503 = temporary model/service availability
        elif "503" in error_text or "UNAVAILABLE" in error_text:

            return {
                "observation": (
                    "The AI vision service is temporarily "
                    "busy."
                ),
                "possible_category": (
                    "AI vision temporarily unavailable"
                ),
                "confidence": "Low",
                "guidance": (
                    "The vision service is experiencing "
                    "temporary high demand."
                ),
                "recommendation": (
                    "Please try the image analysis again "
                    "after a short while."
                ),
                "disclaimer": (
                    "This feature is for health awareness "
                    "only and cannot provide a medical diagnosis."
                )
            }

        # --------------------------------------------------
        # OTHER ERRORS
        # --------------------------------------------------

        else:

            return {
                "observation": (
                    "The AI vision analysis could not "
                    "be completed."
                ),
                "possible_category": (
                    "AI vision unavailable"
                ),
                "confidence": "Low",
                "guidance": (
                    "The visual analysis service "
                    "encountered a temporary problem."
                ),
                "recommendation": (
                    "Please try again later. If the "
                    "problem continues, check the "
                    "Gemini API configuration."
                ),
                "disclaimer": (
                    "This image analysis is for health "
                    "awareness only and cannot provide "
                    "a medical diagnosis."
                )
            }