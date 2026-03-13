import json
import os
import logging

class ConfigManager:
    """Manages saving and loading of build configurations."""
    PROFILE_FILE = "build_profiles.json"

    @staticmethod
    def save_profile(name: str, data: dict) -> bool:
        """Saves a build configuration profile."""
        try:
            profiles = ConfigManager.load_all()
            profiles[name] = data
            with open(ConfigManager.PROFILE_FILE, "w") as f:
                json.dump(profiles, f, indent=4)
            return True
        except Exception as e:
            logging.error(f"Failed to save profile: {e}")
            return False

    @staticmethod
    def load_profile(name: str) -> dict:
        """Loads a specific configuration profile."""
        return ConfigManager.load_all().get(name, {})

    @staticmethod
    def load_all() -> dict:
        """Loads all saved profiles."""
        if not os.path.exists(ConfigManager.PROFILE_FILE):
            return {}
        try:
            with open(ConfigManager.PROFILE_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logging.error("Profile file corrupted. Starting fresh.")
            return {}