import sqlite3
import os
import json

def store_user_input(date=None, text_memory=None):
	try:
		db_path = os.path.join(os.path.dirname(__file__), "storage.db")
		connection = sqlite3.connect(db_path)
		cursor = connection.cursor()

		cursor.execute("""
					   INSERT OR REPLACE INTO user_inputs (date, text)
				 	   VALUES (?, ?)""", (
							date,
							json.dumps(text_memory)
					   ))
		connection.commit()
		connection.close()

	except Exception as ex:
		print(ex)