import datetime as dt
from team_planer.core.config_manager import ConfigManager

# TODO: make the internal logic with one specific date format (create a date format converter)
class DateManager:
	"""
	Utility class for generating formatted date strings relative to the current date.

	The date format is determined from the application configuration and
	applied consistently across all returned strings.

	Attributs:
		config_manager (ConfigManager): Loads the application configuration.
		date_format (str): The format string used for date output (e.g., "dd.mm.yyyy").
	"""

	def __init__(self):
		"""
		Initialize the DateManager and load the configured date format.
		"""
		self.config_manager = ConfigManager()
		config = self.config_manager.load_config()
		self.date_format = config["date_format"]

	# TODO: implement the other date formats
	def get_date_str(self, day: int = 0, date_format: str | None = None) -> str:
		"""
		Return a formatted date string for a given day offset from today.

		Args:
			day (int, optional): The number of days to offset from today.
									Defaults to 0 (today).
		
		Returns:
			str: The formatted date string.

		Notes:
			- Currently, only the "dd.mm.yyyy" format is implemented.
			- Other formats return the string "ERROR".
		"""
		tdate = dt.date.today()
		date = str(tdate + dt.timedelta(day))
		day = date[8:]
		month = date[5:7]
		year_yyyy = date[:4]
		year_yy = date[2:4]

		if date_format is None:
			date_format = self.date_format

		if date_format == "dd.mm.yyyy":
			return f"{day}.{month}.{year_yyyy}"
		elif date_format == "dd/mm/yyyy":
			return f"{day}/{month}/{year_yyyy}"
		elif date_format == "dd.mm.yy":
			return f"{day}.{month}.{year_yy}"
		elif date_format == "dd/mm/yy":
			return f"{day}/{month}/{year_yy}"
		elif date_format == "mm.dd.yyyy":
			return f"{month}.{day}.{year_yyyy}"
		elif date_format == "mm/dd/yyyy":
			return f"{month}/{day}/{year_yyyy}"
		elif date_format == "mm.dd.yy":
			return f"{month}.{day}.{year_yy}"
		elif date_format == "mm/dd/yy":
			return f"{month}/{day}/{year_yy}"		
		else:
			return "ERROR"
			
	def get_date_str_list(self, week: int = 0, date_format: str | None = None):
		if date_format is None:
			date_format = self.date_format

		date_list = []
		tday = dt.date.today()
		weekday = dt.date.today().weekday()
		date_weekday0 = tday - dt.timedelta(weekday) + dt.timedelta(week * 7)
		if date_format == "dd.mm.yyyy":
			for i in range(8):
				date = str(date_weekday0 + dt.timedelta(i))
				date_list.append(f"{date[8:]}.{date[5:7]}.{date[:4]}")
			return date_list
		elif date_format == "ddmmyyyy":
			return "not yet implemented"
		elif date_format == "mmddyyyy":
			return "not yet implemented"
		elif date_format == "ddmmyy":
			return "not yet implemented"
		elif date_format == "mmddyy":
			return "not yet implemented"

if __name__ == "__main__":
	pass