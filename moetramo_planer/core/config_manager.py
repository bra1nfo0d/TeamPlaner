import os
import json

APP_NAME = "moetramoPlaner"
CONFIG_DIR = os.path.join(os.getenv("APPDATA"), APP_NAME)
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
	"today_border_color": "#FFFF00",
	"day_date_label_color": "#FFFFFF",
	"input_types": ["Tour", "Termin", "Lieferung"],
	"input_types_header": {"Tour": ["_", "Fahrzeug", "Monteure", "+Aufträge"],
						   "Termin": ["_", "Mitarbeiter", "Typ", "Zeit"],
						   "Lieferung": ["Lieferung"]},
	"input_types_config": {"Tour": ["#ccc", "#ccc"],
						   "Termin": ["#ccc", "#ccc"],
						   "Lieferung": ["#0000FF", "#ccc"]},
	"calc_value": 1000.00
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