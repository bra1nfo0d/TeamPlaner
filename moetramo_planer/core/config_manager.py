import os
import json

APP_NAME = "moetramoPlaner"
CONFIG_DIR = os.path.join(os.getenv("APPDATA"), APP_NAME)
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
	"language": "de",
	"today_border_color": "#FFFF00",
	"day_date_label_color": "#FFFFFF",
	"first_input_type": "Tour",
	"input_types": {"Tour": [("Tour", 1, "#ccc", "#ccc"), ("_", "text"), ("Fahrzeug", "text"), ("Monteure", "text"), ("Aufträge", ("calc#1000"))],
				 	"Termin": [("Termin", 2, "#ccc", "#ccc"), ("_", "text"), ("Mitarbeiter", "text"), ("Zeit", "text")],
					"Lieferung": [("Lieferung", 3, "#ccc", "#0000FF"), ("Lieferung", "text")]},
	"calc_true_color": "#008000",
	"calc_false_color": "#ff0000"
}

class ConfigManager:
	def __init__(self):
		os.makedirs(CONFIG_DIR, exist_ok=True)
		self.config = self.load_config()

	def load_config(self):
		if not os.path.exists(CONFIG_FILE):
			self.save_config(DEFAULT_CONFIG)
			return DEFAULT_CONFIG
		
		with open(CONFIG_FILE, "r") as f:
			config = json.load(f)

		for key, value in DEFAULT_CONFIG.items():
			config.setdefault(key, value)

		return config

	def save_config(self, config=None):
		if config is None:
			config = self.config
		with open(CONFIG_FILE, "w") as f:
			json.dump(config, f, indent=4)


if __name__ == "__main__":
	pass