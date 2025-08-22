import sqlite3
import os
import json

APP_NAME = "moetramoPlaner"
DATA_DIR = os.path.join(os.getenv("APPDATA"), APP_NAME)  # writable location
DB_FILE = os.path.join(DATA_DIR, "storage.db")

class StorageManager:
	def __init__(self):
		os.makedirs(DATA_DIR, exist_ok=True)

	def create_db(self):
		try:
			connection = sqlite3.connect(DB_FILE)
			cursor = connection.cursor()
			cursor.execute("""
						CREATE TABLE IF NOT EXISTS user_inputs (
						id INTEGER PRIMARY KEY AUTOINCREMENT,
						date TEXT NOT NULL,
						text TEXT,
						config TEXT)
						""")
			connection.commit()
			connection.close()
		except Exception as ex:
			print(ex)

	def laod_user_data(self, date_frame_map=None):
		from widgets.user_input import UserInput
		try:
			connection = sqlite3.connect(DB_FILE)
			cursor = connection.cursor()

			cursor.execute("SELECT date, text, config FROM user_inputs")
			rows = cursor.fetchall()

			for row in rows:
				user_input = UserInput(text_memory=json.loads(row[1]), layout=date_frame_map[row[0]][0], spacer=date_frame_map[row[0]][1], date=row[0], settings=json.loads(row[2]))
				user_input.show_input()
			
			connection.close()
		except Exception as ex:
			print(ex)

	def store_user_input(self, date=None, text_memory=None, config=None):
		try:
			connection = sqlite3.connect(DB_FILE)
			cursor = connection.cursor()

			cursor.execute("""
						INSERT OR REPLACE INTO user_inputs (date, text, config)
						VALUES (?, ?, ?)""", (
								date,
								json.dumps(text_memory),
								json.dumps(config)
						))
			connection.commit()
			connection.close()

		except Exception as ex:
			print(ex)

	def delete_db(self):
		try:
			connection = sqlite3.connect(DB_FILE)
			cursor = connection.cursor()

			cursor.execute("DELETE FROM user_inputs")

			connection.commit()
			connection.close()

		except Exception as ex:
			print(ex)
	
	def delete_user_input(self, date=None, text_memory=None):
		try:
			connection = sqlite3.connect(DB_FILE)
			cursor = connection.cursor()

			json_text = json.dumps(text_memory)

			cursor.execute("""
						DELETE FROM user_inputs
						WHERE date = ? AND text = ?
						""", (
							date,
							json_text
						))
			
			connection.commit()
			connection.close()
		except Exception as ex:
			print(ex)

if __name__ == "__main__":
	pass