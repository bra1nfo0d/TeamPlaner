import os
import json

APP_NAME = "TeamPlaner"
CONFIG_DIR = os.path.join(os.getenv("APPDATA"), APP_NAME)
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

# Default configuration settings for the application
DEFAULT_CONFIG = {				  
	"language": "de",
	"window_title": "moetramo Planer",
	"window_shown": 2,
	"weeks_shown": 2,
	"date_format": "dd.mm.yyyy",
	"weekday_list": (
		"Montag",
		"Dienstag",
		"Mittwoch", 
		"Donnerstag",
		"Freitag"
	),
	"tday_border_color": "#FFFF00",
	"header_color": "#FFFFFF",
	"first_input_type": "Tour",
	"input_types": {
		"Tour": [
			("Tour", 1, "#ccc", "#ccc"),
			("_", "text"),
			("Fahrzeug", "text"),
			("Monteure", "text"),
			("Aufträge", ("calc#1000"))
		],
		"Termin": [
			("Termin", 2, "#ccc", "#ccc"),
			("_", "text"),
			("Mitarbeiter", "text"),
			("Zeit", "text")
		],
		"Lieferung": [
			("Lieferung", 3, "#ccc", "#0000FF"),
			("Lieferung", "text")
		]
	},
	"calc_true_color": "#008000",
	"calc_false_color": "#ff0000",
	"E001": ("Header", "Text"),
	"E002": ("Header", "Text"),
	"E003": ("Header", "Text"),
	"E004": ("Header", "Text")
}

class ConfigManager:
	"""
	Handles loading and saving of application configuration.

	Configurations are stored as JSON in the user's AppData directory.
	If no configuration exists, a default one is created.

	Atrributes:
		config (dict): The currently loaded configuration dictionary.
	"""

	def __init__(self):
		"""
		Initialize the ConfigManager.

		Ensures the config directory exists and loads the configuration.
		If no config file is present, saves the default configuration.
		"""
		os.makedirs(CONFIG_DIR, exist_ok=True)
		self.config = self.load_config()

	def load_config(self) -> dict:
		"""
		Load the configuration from disk.

		Returns:
			dict: The loaded configuration dictionary.
					Falls back to DEFAULT_CONFIG if the file does not exist.
		"""
		if not os.path.exists(CONFIG_FILE):
			self.save_config(DEFAULT_CONFIG)
			return DEFAULT_CONFIG
		
		with open(CONFIG_FILE, "r") as f:
			config = json.load(f)
		
		# Ensure all default keys exist
		for key, value in DEFAULT_CONFIG.items():
			config.setdefault(key, value)

		return config

	def save_config(self, config: dict = None) -> None:
		"""
		Save the configuration to disk.

		Args:
			config (dict, optional): The configuration to save.
										If None, saves the current self.config.
		"""
		if config is None:
			config = self.config
		with open(CONFIG_FILE, "w") as f:
			json.dump(config, f, indent=4)


if __name__ == "__main__":
	pass