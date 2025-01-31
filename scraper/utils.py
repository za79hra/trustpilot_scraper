from bs4 import BeautifulSoup
import json
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()


def load_json(file_path, default=None):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else default
    except FileNotFoundError:
        return default if default is not None else []


def save_json(file_path, data):
    """Save data to a JSON file"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Create folder if it doesn't exist
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def clean_text(text):
    """Clean text from extra characters"""
    cleaned_text = BeautifulSoup(text, "html.parser").get_text()
    return cleaned_text.strip().replace("\n", " ").replace("\r", "")
