from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from core.date_manager import get_date_str
from core.config_manager import ConfigManager
from widgets.clickable_label import ClickableLabel
from windows.input_window import InputWindow

class ColumnDayWidget(QWidget):
	def __init__(self, day, date):
		super().__init__()

		self.config_manager = ConfigManager()

		self.day = day		
		self.date = date	

		self.today_border_color = self.config_manager.load_config()["today_border_color"]
		self.text_color = self.config_manager.load_config()["day_date_label_color"]

		self.frame = QFrame(self)
		self.frame.setFrameShape(QFrame.Box)
		self.frame.setLineWidth(2)
		if get_date_str(day=0) == date:
			self.frame.setStyleSheet(f"""border: 1px solid #ccc;
										 border-radius: 10px;
										 border-color: {self.today_border_color};""")
		else:	
			self.frame.setStyleSheet("""border: 1px solid #ccc;
										border-radius: 10px;								
									""")

		self.frame_layout = QVBoxLayout(self.frame)
		self.frame_layout.setContentsMargins(8, 8, 8, 8)
		self.frame_layout.setSpacing(4)

		main_layout = QVBoxLayout(self)
		main_layout.addWidget(self.frame)

		self.add_label()
		self.add_spacer()

	def add_spacer(self):
		self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.frame_layout.addItem(self.spacer)

	def add_label(self):
		padding_layout = QVBoxLayout()
		padding_layout.setContentsMargins(0, 0, 0, 10)
		
		label = ClickableLabel(f"{self.day}\n{self.date}")
		label.setAlignment(Qt.AlignCenter)
		label.setFont(QFont("Arial", 10, QFont.Bold))
		if get_date_str(0) == self.date:
			label.setStyleSheet(f"""padding: 4px; 
									border: 2px solid {self.today_border_color};
									border-radius: 10px;
									color: {self.text_color};""")
		else:
			label.setStyleSheet(f"""padding: 4px; 
									border: 1px solid #ccc;
									border-radius: 10px;
									color: {self.text_color};""")
		label.clicked.connect(self.label_clicked)
		padding_layout.addWidget(label)
		self.frame_layout.addLayout(padding_layout)
	
	def label_clicked(self):
#		from core.window_controller import WindowController
		input_window = InputWindow(self.day, self.date, self.frame_layout, self.spacer)
		input_window.show()
#		self.window_controller = WindowController()
#		self.window_controller.start_input_window(self.day, self.date, self.frame_layout, self.spacer)
	
	def return_date_frame_widgets(self):
		return [self.date, self.frame_layout, self.spacer]
	
if __name__ == "__main__":
	pass