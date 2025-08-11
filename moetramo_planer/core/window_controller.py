from windows.week_overview import WeekOverview
from windows.input_window import InputWindow
from windows.edit_window import EditWindow

class WindowController:
	def __init__(self):
		pass

	def start_week_overview(self):
		self.week_overview = WeekOverview(weeks=2)
		self.week_overview.showMaximized()
	
	def get_frame_date_map(self):
		return self.week_overview.get_date_frame_map()
	
	def start_input_window(self, day, date, frame_layout, spacer):
		self.input_window = InputWindow(day, date, frame_layout, spacer)
		self.input_window.show()
	
	def start_edit_window(self, day, date, target_frame, target_spacer):
		edit_window = EditWindow(day, date, target_frame, target_spacer)

if __name__ == "__main__":
	pass