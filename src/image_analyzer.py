from PIL import Image


def validate_image(image):
    """
    Validate an uploaded image.
    """

    if image is None:
        return {
            "valid": False,
            "message": "No image was uploaded."
        }

    try:
        img = Image.open(image)

        width, height = img.size

        if width < 150 or height < 150:
            return {
                "valid": False,
                "message": (
                    "The image is too small. "
                    "Please upload a clearer image."
                )
            }

        return {
            "valid": True,
            "message": "Image is suitable for analysis.",
            "width": width,
            "height": height,
            "format": img.format
        }

    except Exception:
        return {
            "valid": False,
            "message": "The uploaded file could not be read as an image."
        }