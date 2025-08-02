from windows.week_overview import WeekOverview
from windows.input_window import InputWindow

class WindowController:
	def __init__(self):
		pass

	# opens the main window
	def start_week_overview(self):
		self.week_overview = WeekOverview(weeks=2)
		self.week_overview.showMaximized()
	
	def get_frame_date_map(self):
		return self.week_overview.get_date_frame_map()
	
	# opens the input window
	def start_input_window(self, day, date, frame_layout, spacer):
		self.input_window = InputWindow(day, date, frame_layout, spacer)
		self.input_window.show()

if __name__ == "__main__":
	pass