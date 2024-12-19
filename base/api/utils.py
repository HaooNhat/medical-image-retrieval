import os

import cloudinary.api

from dotenv import load_dotenv

load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),  # Replace with your Cloudinary cloud name
    api_key=os.getenv("API_KEY"),        # Replace with your Cloudinary API key
    api_secret=os.getenv("API_SECRET")   # Replace with your Cloudinary API secret
)


def remove_extension(filename):
    """
    Removes the file extension from the given filename string.

    :param filename: The filename as a string (e.g., "image.png").
    :return: The filename without the extension (e.g., "image").
    """
    return filename.rsplit('.', 1)[0]

def find_image_from_cloudinary(filename):
    try:
        # Search for the image by public_id
        response = cloudinary.api.resource(f"my_medical_images/{remove_extension(filename)}")
        return response["secure_url"]
    except Exception as e:
        print(f"Image not found: {e}")
