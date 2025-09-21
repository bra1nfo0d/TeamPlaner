from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget
from PySide6.QtGui import QKeySequence, QShortcut
from widgets.column_day_widget import ColumnDayWidget
from core.date_manager import get_date_str_list
from core.storage_manager import StorageManager

class WeekOverview(QMainWindow):
	def __init__(self, weeks=1):
		super().__init__()
		self.cur_week_code = 0
		self.weeks = weeks	
		self.date_frame_map = {}
		self.cur_week_widgets = []

		self.storage_manager = StorageManager()

		self.setWindowTitle("moetramo Planer") 

		central_widget = QWidget()
		self.widget_layout = QHBoxLayout()
		central_widget.setLayout(self.widget_layout)
		self.setCentralWidget(central_widget)

		shortcut_left = QShortcut(QKeySequence("Left"), self)
		shortcut_left.activated.connect(lambda: self.on_week_change("past"))
		shortcut_right = QShortcut(QKeySequence("Right"), self)
		shortcut_right.activated.connect(lambda: self.on_week_change("future"))

		self.create_weekdays()
	
	def create_weekdays(self):
		days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
		for i in range(2):
			for j in range(len(days)):
				day_widget = ColumnDayWidget(days[j], get_date_str_list(i+self.cur_week_code)[j])
				self.widget_layout.addWidget(day_widget)	
				date_frame_list = day_widget.return_date_frame_widgets() 
				self.date_frame_map[date_frame_list[0]] = (date_frame_list[1], date_frame_list[2])
				self.cur_week_widgets.append(day_widget)
	
	def get_date_frame_map(self):
		return self.date_frame_map
	
	def on_week_change(self, direction):
		if direction == "past":
			x = -1
		elif direction == "future":
			x = 1
		self.cur_week_code += x
		for widget in self.cur_week_widgets:
			widget.setParent(None)
			widget.deleteLater()
		self.cur_week_widgets = []
		self.date_frame_map = {}
		self.create_weekdays()
		self.storage_manager.laod_user_data(date_frame_map=self.date_frame_map)
		print(self.cur_week_code)
	
if __name__ == "__main__":
	pass