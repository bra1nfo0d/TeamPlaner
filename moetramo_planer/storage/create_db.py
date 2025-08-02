import sqlite3
import os

def create_db():
	try:
		db_path = os.path.join(os.path.dirname(__file__), "storage.db")
		connection = sqlite3.connect(db_path)
		cursor = connection.cursor()

		cursor.execute("""
					   CREATE TABLE IF NOT EXISTS user_inputs (
				 	   id INTEGER PRIMARY KEY AUTOINCREMENT,
				 	   date TEXT NOT NULL,
					   text TEXT)
				 	   """)
		connection.commit()
		connection.close()
		
	except Exception as ex:
		print(ex)

if __name__ == "__main__":
	pass