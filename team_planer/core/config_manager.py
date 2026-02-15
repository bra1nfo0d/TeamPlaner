import os
import json

APP_NAME = "TeamPlaner"
CONFIG_DIR = os.path.join(os.getenv("APPDATA"), APP_NAME)
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

# Default configuration settings for the application
DEFAULT_CONFIG = {
	"language": "de",
	"window_title": "TeamPlaner",
	"window_shown": 1,
	"weeks_shown": 2,
	"date_format": "dd.mm.yyyy",
	"show_holidays": True,
	"weekday_list": (
		"Montag",
		"Dienstag",
		"Mittwoch", 
		"Donnerstag",
		"Freitag"
	),
	"input_goal_per_worker" : 500,

	"display-window_font-size": 10,
	"display-window_font-family": "Arial",
	"display-window_font-weight": "Bold",
	"display-window_content-frame_border-width": 1,
	"display-window_content-frame_border-radius": 5,
	"display-window_content-frame_border-color": "#ccc",
	"display-window_tday-content-frame_border-color": "#FFFF00",
	"display-window_header-frame_border-width": 1,
	"display-window_header-frame_border-radius": 5,
	"display-window_header-frame_border-color": "#ccc",
	"display-window_tday-header-frame_border-color": "#FFFF00",
	"display-window_header-frame_padding": 4,
	"display-window_header-content_margin": 10,
	"display-window_frame-content_margin": [8, 8, 8, 8],
	"display-window_content-content_margin": 4,

	"user-input_font-size": 12,
	"user-input_font-family": "Arial",
	"user-input_font-weight": "Regular",
	"user-input_inner-border-width": 1,
	"user-input_inner-border-radius": 2,
	"user-input_inner-border-color": "#ccc",
	"user-input_outer-border-width": 1,
	"user-input_outer-border-radius": 2,
	"user-input_outer-border-color": "#ccc",
	"user-input_calc-true-color": "#008000",
	"user-input_calc-false-color": "#ff0000",

	"edit-window_font-size": 10,
	"edit-window_font-family": "Arial",
	"edit-window_font-weight": "Regular",
	"edit-window_inner-border-width": 1,
	"edit-window_inner-border-radius": 10,
	"edit-window_inner-border-color": "#ccc",
	"edit-window_outer-border-width": 1,
	"edit-window_outer-border-radius": 10,
	"edit-window_outer-border-color": "#ccc",
	"edit-window_focused-content-color": "#FFFF00",
	"edit-window_unchangeable-content-color": "#435663",
	"edit-window_content-margin": [5, 2, 5, 2],

	"input-window_font-size": 10,
	"input-window_font-family": "Arial",
	"input-window_font-weight": "Regular",
	"input-window_inner-border-width": 1,
	"input-window_inner-border-radius": 10,
	"input-window_inner-border-color": "#ccc",
	"input-window_outer-border-width": 1,
	"input-window_outer-border-radius": 10,
	"input-window_outer-border-color": "#ccc",
	"input-window_focus-content-color": "#FFFF00",
	"input-window_content-margin": [5, 2, 5, 2],
	"input-window_input-types": {
		"Tour": [
			("Tour", 1, "#ccc", "#ccc"),
			("_", "text"),
			("Fahrzeug", "text"),
			("Monteure", "worker"),
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
	"input-window_first-input-type": "Tour",
	
	"Error-Massages": {
		0: ("Verbotene Eingabeform", "Die Nutzereingabe darf nicht mit einem * beginnen."),
		1: ("Falsche Eingabeform", "Fehler bei einer Calculations-Eingabe. Die Eingabe muss\ndie From <Titel>#<Betrag> haben."),
		2: ("Verbotene Eingabeform", "Die Eingabe darf nicht leer sein."),
		3: ("Ungültiger Eingabetyp", "Der Eingabetyp ist in einem Ungültigen Format."),
		4: ("Verlerhafte Eingabe", "Ein Eingabefeld wurde leer gelassen.") 
	},
	"Warning-Massages": {
		0: ("Eintrag Löschen", "Dieser Eintrag wird unwiederuflich gelöscht.")
	},



	"user_display_input_font_size": 1,
	"user_display_input_border_width": 1,
	"user_display_input_border_radius": 5,
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
	"E004": ("Header", "Text"),
	"E005": ("Configurations Fehler", "Falsche Eingabe in der Configurations-Datei!")
}

class ConfigManager:
	"""Manages loading and saving the app config."""

	def __init__(self):
		"""Initialize ConfigManager."""
		os.makedirs(CONFIG_DIR, exist_ok=True)
		self.config = self.load_config()

	def load_config(self) -> dict:
		"""
		Load the configuration file or create a default one.

		Returns:
			dict: The current configuration.
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
			config (dict, optional): Config to save. Defaults to self.config.
		"""
		if config is None:
			config = self.config
		with open(CONFIG_FILE, "w") as f:
			json.dump(config, f, indent=4)


if __name__ == "__main__":
	pass