from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QLabel, QWidget
from widgets.column_day_widget import ColumnDayWidget
from core.date_manager import get_date_str_list

class WeekOverview(QMainWindow):
	def __init__(self, weeks=1):
		super().__init__()
		self.weeks = weeks	# number of weeks shown

		self.date_frame_map = {}

		# window settings
		self.setWindowTitle("moetramo Planer") # titel of the main screen

		# layout
		central_widget = QWidget()
		self.widget_layout = QHBoxLayout()
		central_widget.setLayout(self.widget_layout)
		self.setCentralWidget(central_widget)

		# starts the day display
		self.create_weekdays()
	
	# creates the weekdays
	def create_weekdays(self):
		days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
		for week in range(self.weeks):
			for i in range(len(days)):
				day_widget = ColumnDayWidget(days[i], get_date_str_list(week)[i])
				self.widget_layout.addWidget(day_widget)	# gets the date frame info, for every day on display
				date_frame_list = day_widget.return_date_frame_widgets() 
				self.date_frame_map[date_frame_list[0]] = (date_frame_list[1], date_frame_list[2]) # creates the date frame map
	
	def get_date_frame_map(self):
		return self.date_frame_map
	
if __name__ == "__main__":
	pass