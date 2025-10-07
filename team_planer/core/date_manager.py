import datetime as dt
from team_planer.core.config_manager import ConfigManager

# TODO: make the internal logic with one specific date format (create a date format converter)
class DateManager:
	"""Utility class for generating formatted date strings."""

	def __init__(self):
		"""Load config and set the active date format."""
		self.config_manager = ConfigManager()
		config = self.config_manager.load_config()
		self.date_format = config["date_format"]

	# TODO: implement the other date formats
	def get_date_str(self, day: int = 0, date_format: str | None = None) -> str:
		"""
		Get a formatted date string for a given day offset.

		Args:
			day (int, optional): Days offset from today. Defaults to 0.
			date_format (str, optional): Custom format override.

		Returns:
			str: The formatted date string.
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
			return "format error"
			
	def get_date_str_list(self, week: int = 0, date_format: str | None = None):
		"""
		Get a list of formatted date strings for a given week.

		Args:
			week (int, optional): Week offset form current week. Default to 0.

		Returns:
			list[str]: List of formatted date strings.
		"""
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
		elif date_format in {
			"dd.mm.yyyy", "dd//mm//yyyy",
			"dd.mm.yy", "dd/mm/yy",
			"mm.dd.yyyy", "mm/dd/yyyy",
			"mm.dd.yy", "mm/dd/yy"
		}:
			return ["format not yet implemented" * 7]
		else:
			return ["format error" * 7]

if __name__ == "__main__":
	pass