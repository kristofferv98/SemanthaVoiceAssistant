import json
import logging


class ConfigurationManager:
    def __init__(self, filename: str = 'Config/config_file.json'):
        self.filename = filename
        self.config = self.load_config()
        self._updated_keys_values = {}

    def load_config(self) -> dict:
        try:
            with open(self.filename, 'r') as file:
                file_content = file.read()
                return json.loads(file_content) if file_content else {}
        except FileNotFoundError:
            logging.error(f"Configuration file '{self.filename}' not found. Starting with an empty configuration.")
            return {}
        except json.JSONDecodeError as e:
            logging.error(
                f"Error decoding JSON from the file '{self.filename}': {e}. Starting with an empty configuration.")
            return {}

    def get_config(self, key: str, default=None):
        return self.config.get(key, default)

    def set_config(self, key: str, value):
        if key not in self.config or self.config[key] != value:
            self.config[key] = value
            self._updated_keys_values[key] = value
            logging.debug(f"Configuration updated for key: {key}")
            self.save_config()

    def check_updated_configs(self) -> dict:
        return self._updated_keys_values

    def reset_updated_configs(self):
        self._updated_keys_values.clear()
        logging.debug("Updated configuration tracking reset.")

    def save_config(self):
        try:
            with open(self.filename, 'w') as file:
                self.config.update(self._updated_keys_values)
                json.dump(self.config, file, indent=4)
        except (FileNotFoundError, PermissionError, IOError) as e:
            logging.error(f"Error saving configuration to file: {e}")

    def clear_config(self):
        # Add a safety check or confirmation if needed
        self.config = {}
        self.save_config()
        logging.info("Configuration file content cleared.")

    def toggle(self, key: str, options: tuple):
        """
        Toggles the configuration setting between two options.

        :param key: The key in the configuration to toggle.
        :param options: A tuple containing two possible values to toggle between.
        """
        current_value = self.get_config(key, options[0])  # Default to the first option if not set
        new_value = options[1] if current_value == options[0] else options[0]
        self.set_config(key, new_value)
        logging.info(f"{key} toggled to: {new_value}")

    def toggle_input_mode(self):
        """
        Toggles the input mode between 'typing' and 'recording'.
        """
        self.toggle('input_mode', ('typing', 'recording'))

    def toggle_voice_feedback(self):
        """
        Toggles the voice feedback between 'on' and 'off'.
        """
        self.toggle('voice_feedback', (True, False))