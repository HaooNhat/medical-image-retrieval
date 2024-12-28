import os

import cloudinary.api
import cloudinary.uploader

from dotenv import load_dotenv

load_dotenv()

import random

import re

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),  # Replace with your Cloudinary cloud name
    api_key=os.getenv("API_KEY"),        # Replace with your Cloudinary API key
    api_secret=os.getenv("API_SECRET")   # Replace with your Cloudinary API secret
)

def generate_custom_id():
    return random.randint(10**17, 10**18 - 1)

def transform_text(text):
    # Remove redundant spaces
    text = re.sub(r'\s+', ' ', text).strip()
    # Replace ", " with "|"
    text = text.replace(", ", "|")
    # Replace " " with "_"
    text = text.replace(" ", "_")
    return text

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
        

def upload_single_image(image_file):
    try:
        # Upload the image to Cloudinary
        response = cloudinary.uploader.upload(
            image_file,
            folder="my_medical_images",  # Target folder in Cloudinary
            use_filename=True,         # Retain the original filename
            unique_filename=False      # Avoid adding random characters
        )
        secure_url = response["secure_url"]
        print(f"Uploaded: {image_file.name} -> {secure_url}")
        return secure_url
    except Exception as e:
        print(f"Failed to upload {image_file.name}: {e}")
        raise  # Re-raise the exception for proper error handling


def calculate_probs(results):
    # Initialize a dictionary to count occurrences of each disease
    label_counts = {}

    # Iterate through each record
    for record in results:
        labels = record["labels"]
        # Split multiple labels and normalize them
        diseases = [label.replace("_", " ") for label in labels.split("|")]
        for disease in diseases:
            label_counts[disease] = label_counts.get(disease, 0) + 1

    # Calculate percentages
    total_records = len(results)
    total_disease_instances = sum(label_counts.values())  # Total diseases (may exceed records)
    label_percentages = {
        label: (count / total_disease_instances) * 100 for label, count in label_counts.items()
    }
    
    # print(label_percentages)
    return label_percentages