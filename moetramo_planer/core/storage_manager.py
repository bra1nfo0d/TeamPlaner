from storage.create_db import create_db
from storage.load_user_inputs import load_user_inputs
from storage.store_user_input import store_user_input
from storage.delete_db import delete_db
from storage.delete_user_input import delete_user_input

class StorageManager:
	def __init__(self):
		pass

	def create_db(self):
		create_db()

	def laod_user_data(self, date_frame_map=None):
		load_user_inputs(date_frame_map=date_frame_map)

	def store_user_input(self, date=None, text_memory=None):
		store_user_input(date=date, text_memory=text_memory)

	def delete_db(self):
		delete_db()
	
	def delete_user_input(self, date=None, text_memory=None):
		delete_user_input(date=date, text_memory=text_memory)