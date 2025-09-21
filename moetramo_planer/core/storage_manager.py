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
				  		type TEXT,
						settings TEXT,
						text TEXT)
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

			dates = list(date_frame_map.keys())
			placeholder = ",".join("?" for _ in dates)
			query = f"SELECT date, type, settings, text FROM user_inputs WHERE date IN ({placeholder})"
			cursor.execute(query, dates)
			
			rows = cursor.fetchall()
			
			for row in rows:
				user_input = UserInput(text_memory=json.loads(row[3]), layout=date_frame_map[row[0]][0], spacer=date_frame_map[row[0]][1], date=row[0], settings=json.loads(row[2]))
				user_input.show_input()

			
			connection.close()
		except Exception as ex:
			print(ex)

	def store_user_input(self, date=None, text_memory=None, settings=None):
		try:
			connection = sqlite3.connect(DB_FILE)
			cursor = connection.cursor()

			cursor.execute("""
						INSERT OR REPLACE INTO user_inputs (date, type, settings, text)
						VALUES (?, ?, ?, ?)""", (
								date,
								settings[0],
								json.dumps(settings),
								json.dumps(text_memory)
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