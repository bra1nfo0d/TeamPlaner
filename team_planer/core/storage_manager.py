import sqlite3
import os
import json
from team_planer.windows.warning_window import PopupWindow

APP_NAME = "TeamPlaner"
DATA_DIR = os.path.join(os.getenv("APPDATA"), APP_NAME)
DB_FILE = os.path.join(DATA_DIR, "storage.db")

class StorageManager:
	"""Handles reading and writing user data to the SQLite database."""

	# TODO: Change the doc with parent
	def __init__(self, parent: object | None = None):
		"""
		Args:
			parent (object | None): Parent window or controller.
		"""
		self.parent = parent
		os.makedirs(DATA_DIR, exist_ok=True)

	def create_db(self) -> None:
		"""Create the database and 'user_inputs' table if not existing."""
		try:
			connection = sqlite3.connect(DB_FILE)
			cursor = connection.cursor()
			cursor.execute("""
				  CREATE TABLE IF NOT EXISTS user_inputs (
				  id INTEGER PRIMARY KEY AUTOINCREMENT,
				  date TEXT NOT NULL,
				  type TEXT,
				  settings TEXT,
				  text TEXT
				  )
			""")
			connection.commit()
			connection.close()
		except Exception as ex:
			self.show_warning("E004")

	def load_user_data(self, date_frame_connection: map) -> None:
		"""
		Load user inputs from the database into connected UI frames.

		Args:
			date_frame_connection (map): Maps a date string to (layout, spacer).
		"""
		from team_planer.ui_elements.user_input import UserInput
		try:
			connection = sqlite3.connect(DB_FILE)
			cursor = connection.cursor()
			dates = list(date_frame_connection.keys())
			placeholder = ",".join("?" for _ in dates)
			query = f"""
				SELECT date, type, settings, text
				FROM user_inputs
				WHERE date IN ({placeholder})
			"""
			cursor.execute(query, dates)			
			rows = cursor.fetchall()

			for row in rows:
				user_input = UserInput(
					row[0],
					json.loads(row[3]),
					json.loads(row[2]),
					date_frame_connection[row[0]][0],
					date_frame_connection[row[0]][1]
				)
				user_input._show_input()

			connection.close()
		except Exception as ex:
			self.show_warning("E004")

	def store_user_input(self, date: str, text_memory: list[list[str]], settings: list[str]) -> None:
		"""
		Store a user input entry.

		Args:
			date (str): Input date.
			text_memory (list[list[str]]): Input content.
			settings (list[str]): Input metadata.
		"""
		try:
			connection = sqlite3.connect(DB_FILE)
			cursor = connection.cursor()
			cursor.execute("""
				  INSERT INTO user_inputs (date, type, settings, text)
				  VALUES (?, ?, ?, ?)
			""", (
				date,
				settings[0],
				json.dumps(settings),
				json.dumps(text_memory)
			))
			connection.commit()
			connection.close()
		except Exception as ex:
			self.show_warning("E004")

	def delete_db(self) -> None:
		"""Delete all entries form the database."""
		try:
			connection = sqlite3.connect(DB_FILE)
			cursor = connection.cursor()
			cursor.execute("DELETE FROM user_inputs")
			connection.commit()
			connection.close()
		except Exception as ex:
			self.show_warning("E004")
	
	def delete_user_input(self, date: str, text_memory: list[list[str]]) -> None:
		"""
		Delete a specific user input.

		Args:
			date (str): Date of the entry.
			text_memory (list[list[str]]): Input content to match.
		"""
		try:
			connection = sqlite3.connect(DB_FILE)
			cursor = connection.cursor()
			json_text = json.dumps(text_memory)
			cursor.execute("""
				  DELETE FROM user_inputs
				  WHERE date = ? AND text = ?
			""", (date, json_text))			
			connection.commit()
			connection.close()
		except Exception as ex:
			self.show_warning("E004")
	
	def show_warning(self, error_code: str) -> None:
		"""
		Display an error window.

		Args:
			error_code (str): Error code to display.
		"""
		error_window = PopupWindow("error", error_code, self.parent)
		error_window.exec()


if __name__ == "__main__":
	pass