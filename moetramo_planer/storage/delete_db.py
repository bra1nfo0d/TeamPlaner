import sqlite3
import os

def delete_db():
	try:
		db_path = os.path.join(os.path.dirname(__file__), "storage.db")
		connection = sqlite3.connect(db_path)
		cursor = connection.cursor()

		cursor.execute("DELETE FROM user_inputs")

		connection.commit()
		connection.close()

	except Exception as ex:
		print(ex)