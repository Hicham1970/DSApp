import json
import os

CONFIG_FILE = "config.json"


def save_config(settings: dict):
    """Saves the configuration dictionary to a JSON file."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")


def load_config() -> dict:
    """Loads the configuration from a JSON file."""
    if not os.path.exists(CONFIG_FILE):
        return {}  # Return empty dict if file doesn't exist
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading config, using defaults: {e}")
        return {}
