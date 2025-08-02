import sqlite3
import os
import json


def load_user_inputs(date_frame_map=None):
	from widgets.user_input import UserInput
	try:
		db_path = os.path.join(os.path.dirname(__file__), "storage.db")
		connection = sqlite3.connect(db_path)
		cursor = connection.cursor()

		cursor.execute("SELECT date, text FROM user_inputs")
		rows = cursor.fetchall()

		for row in rows:
			user_input = UserInput(text_memory=json.loads(row[1]), layout=date_frame_map[row[0]][0], spacer=date_frame_map[row[0]][1], date=row[0])
			user_input.show_input()
		
		connection.close()
	except Exception as ex:
		print(ex)

if __name__ == "__main__":
	pass