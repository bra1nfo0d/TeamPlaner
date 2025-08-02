import sqlite3
import os
import json

def delete_user_input(date=None, text_memory=None):
	try:
		db_path = os.path.join(os.path.dirname(__file__), "storage.db")
		connection = sqlite3.connect(db_path)
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