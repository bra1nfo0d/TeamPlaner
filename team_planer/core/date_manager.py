import datetime as dt
from core.config_manager import ConfigManager

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
	def get_date_str(self, day: int = 0) -> str:
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
		tday = dt.date.today()
		date = str(tday + dt.timedelta(day))

		if self.date_format == "dd.mm.yyyy":
			return f"{date[8:]}.{date[5:7]}.{date[:4]}"
		
		elif self.date_format == "dd/mm/yyyy":
			return "ERROR"
		elif self.date_format == "dd.mm.yy":
			return "ERROR"
		elif self.date_format == "dd/mm/yy":
			return "ERROR"
		elif self.date_format == "mm.dd.yyyy":
			return "ERROR"
		elif self.date_format == "mm/dd/yyyy":
			return "ERROR"
		elif self.date_format == "mm.dd.yy":
			return "ERROR"
		elif self.date_format == "mm/dd/yy":
			return "ERROR"
		else:
			return "ERROR"

	# TODO: implement the other date formats
	def get_date_str_list(self, week: int = 0) -> list[str]:
		"""
		Return a list of formatted date strings for a given week offset.

		Args:
			week (int, optional): The number of weeks to offset from the current week.
									Defaults to 0 (current week).
		
		Returns:
			list[str]: A list of 8 formatted date strings representing the days
						of the week (starting from Monday).

		Notes:
			- Currently, only the "dd.mm.yyyy" format is implemented.
			- Other formats return the string "ERROR".
		"""
		date_list = []
		tday = dt.date.today()
		weekday = dt.date.today().weekday()
		date_weekday0 = tday - dt.timedelta(weekday) + dt.timedelta(week * 7)

		if self.date_format == "dd.mm.yyyy":
			for i in range(8):
				date = str(date_weekday0 + dt.timedelta(i))
				date_list.append(f"{date[8:]}.{date[5:7]}.{date[:4]}")
			return date_list
		
		elif self.date_format == "dd/mm/yyyy":
			return "ERROR"
		elif self.date_format == "dd.mm.yy":
			return "ERROR"
		elif self.date_format == "dd/mm/yy":
			return "ERROR"
		elif self.date_format == "mm.dd.yyyy":
			return "ERROR"
		elif self.date_format == "mm/dd/yyyy":
			return "ERROR"
		elif self.date_format == "mm.dd.yy":
			return "ERROR"
		elif self.date_format == "mm/dd/yy":
			return "ERROR"
		else:
			return "ERROR"


if __name__ == "__main__":
	pass