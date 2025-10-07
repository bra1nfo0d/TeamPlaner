import json, os, pytest
from team_planer.core.config_manager import ConfigManager, CONFIG_FILE, DEFAULT_CONFIG

@pytest.fixture
def temp_config_dir(tmp_path, monkeypatch):
	"""Create temporary config path for isolated testing."""
	test_dir = tmp_path / "TeamPlanerTest"
	test_file = test_dir / "config.json"
	monkeypatch.setattr("team_planer.core.config_manager.CONFIG_DIR", str(test_dir))
	monkeypatch.setattr("team_planer.core.config_manager.CONFIG_FILE", str(test_file))
	return test_file

def test_load_config_creates_file_with_defaults():
	"""Ensure config loads defaults and creates file if missing."""
	cm = ConfigManager()
	config = cm.load_config()

	assert set(config.keys()) == set(DEFAULT_CONFIG.keys())

	def normalize(value):
		if isinstance(value, tuple):
			return list(value)
		if isinstance(value, dict):
			return {k: normalize(v) for k, v in value.items()}
		if isinstance(value, list):
			return [normalize(v) for v in value]
		return value

	for key, default_value in DEFAULT_CONFIG.items():
		assert normalize(default_value) == normalize(config[key])

def test_save_config_overwrites_file(temp_config_dir):
	"""Verify that saving updates the config file"""
	cm = ConfigManager()
	cm.config["language"] = "en"
	cm.save_config()

	with open(temp_config_dir, "r") as f:
		saved = json.load(f)

	assert saved["language"] == "en"