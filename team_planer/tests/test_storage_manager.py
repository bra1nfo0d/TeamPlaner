import sqlite3, json, pytest
from unittest.mock import patch, MagicMock
from team_planer.core import storage_manager as sm_mod
from team_planer.core.storage_manager import StorageManager

@pytest.fixture
def temp_db(tmp_path, monkeypatch):
	"""Creates temporary SQLite DB and initialize schema."""
	test_db = tmp_path / "test_storage.db"
	monkeypatch.setattr(sm_mod, "DB_FILE", str(test_db))
	sm = StorageManager()
	sm.create_db()
	return sm

def test_create_db_creates_table():
	"""Ensure 'user_inputs' table is created."""
	connection = sqlite3.connect(sm_mod.DB_FILE)
	cursor = connection.cursor()
	cursor.execute("""
				SELECT name FROM sqlite_master
				WHERE type='table'
				AND name='user_inputs'
	""")
	assert cursor.fetchone() is not None
	connection.close()

def test_store_and_load_user_input(temp_db):
	"""Insert and read back stored user input."""
	date = "01.01.2025"
	text_memory = [["text", "test_header"]]
	settings = ["set_1", "set_2", "set_3", "set_4"]
	
	sm = temp_db
	sm.store_user_input(
		date, text_memory, settings
	)

	connection = sqlite3.connect(sm_mod.DB_FILE)
	cursor = connection.cursor()
	cursor.execute("""
		SELECT date, settings, text
		FROM user_inputs WHERE date=?""",
		(date,))
	row = cursor.fetchone()
	
	assert row is not None
	assert row[0] == date
	assert json.loads(row[1]) == settings
	assert json.loads(row[2]) == text_memory

	connection.close()

def test_delete_user_input(temp_db):
	"""Delete a specific user input entry."""
	date = "01.01.2025"
	text_memory = [["text", "test_header"]]
	settings = ["set_1", "set_2", "set_3", "set_4"]
	
	sm = temp_db
	sm.store_user_input(
		date, text_memory, settings
	)
	sm.delete_user_input(
		date, text_memory
	)

	connection = sqlite3.connect(sm_mod.DB_FILE)
	cursor = connection.cursor()
	cursor.execute("""
			SELECT * FROM user_inputs WHERE date=?""",
			(date,))
	row = cursor.fetchone()

	assert row is None

	connection.close()

def test_load_user_date_creates_user_input(temp_db, monkeypatch):
	"""Verify loading user data instantiates UserInput and calls '_show_input'."""
	date = "01.01.2025"
	text_memory = [["text", "test_header"]]
	settings = ["set_1", "set_2", "set_3", "set_4"]
	dummy_layout = object()
	dummy_spacer = object()
	dfc = {"01.01.2025": (dummy_layout, dummy_spacer)}

	sm = temp_db
	sm.store_user_input(
		date, text_memory, settings
	)

	test_user_input = MagicMock()
	monkeypatch.setattr("team_planer.ui_elements.clickable_widgets.UserInput", test_user_input)
	
	sm.load_user_data(dfc)

	test_user_input.assert_called_once_with(
		date,
		text_memory,
		settings,
		dummy_layout,
		dummy_spacer
	)
	test_user_input.return_value._show_input.assert_called_once()