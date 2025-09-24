import sqlite3
import os
import json
from windows.error_window import ErrorWindow

APP_NAME = "TeamPlaner"
DATA_DIR = os.path.join(os.getenv("APPDATA"), APP_NAME)
DB_FILE = os.path.join(DATA_DIR, "storage.db")

class StorageManager:
	"""
	Handles saving and loading user input data to a SQLite database.

	The database stores user inputs with date, type, settings, and text content.
	Data is serialized to JSON for storage and deserialized on load.
	"""

	# TODO: Change the doc with parent
	def __init__(self, parent: object | None = None):
		"""
		Initialize the StorageManager.

		Ensures that the data directory exists so the database file can be created.
		"""
		self.parent = parent
		os.makedirs(DATA_DIR, exist_ok=True)

	def create_db(self) -> None:
		"""
		Create the database schema if it does not exist.

		Creates a table `user_inputs` with the following columns:
			- id (int, primary key, autoincrement)
			- date (str, required): Date associated with the input.
			- type (str): The type/category of the input.
			- settings (str): JSON-encoded settings for the input.
			- text (str): JSON-encoded user input data.
		"""
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
			print(ex, "create_db")

	def load_user_data(self, date_frame_connection: map) -> None:
		"""
		Load user data from the database and render it in the UI.

		Args:
			date_frame_connection (map): Maps a date string to a tuple
											(layout, spacer) for UI rendering.
							
		Side Effects:
			- Queries database for all inputs matching provided dates.
			- Creates `UserInput` objects for each entry.
			- Injects them into the corresponding frame in the UI.
		"""
		from widgets.user_input import UserInput
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
			print(ex, "load_db")

	def store_user_input(self,
					  date: str,
					  text_memory: list[list[str]],
					  settings: list[str]) -> None:
		"""
		Save a new user input to the database.

		If an entry with the same date and type already exists,
		it will be replaced.

		Args:
			date (str): Date of the input.
			text_memory (list[list[str]]): Nested list of user input data.
			settings (list[str]): Input configuration (JSON-encoded).
		"""
		try:
			connection = sqlite3.connect(DB_FILE)
			cursor = connection.cursor()
			cursor.execute("""
				  INSERT OR REPLACE INTO user_inputs (date, type, settings, text)
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
			print(ex)

	def delete_db(self) -> None:
		"""
		Delete all entries from the database.

		Warnings:
			This clears the entire `user_inputs` table.
		"""
		try:
			connection = sqlite3.connect(DB_FILE)
			cursor = connection.cursor()
			cursor.execute("DELETE FROM user_inputs")
			connection.commit()
			connection.close()
		except Exception as ex:
			self.show_warning("E004")
			print(ex)
	
	def delete_user_input(self, date: str, text_memory: list[list[str]]) -> None:
		"""
		Delete a specific user input from the database.

		Args:
			date (str): Date of the input to delete.
			text_memory (list[list[str]]): The content of the input
											(must match JSON stored in DB).
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
			print(ex)
	
	def show_warning(self, error_code: str) -> None:
		error_window = ErrorWindow(error_code, self.parent)
		error_window.exec()


if __name__ == "__main__":
	pass