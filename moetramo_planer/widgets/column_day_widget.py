from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
from core.date_manager import get_date_str
from widgets.clickable_label import ClickableLabel

class ColumnDayWidget(QWidget):
	def __init__(self, day, date):
		super().__init__()

		self.day = day		# day of the column
		self.date = date	# date of the column

		# changes the boarder-color if its the current day
		if get_date_str(day=0) == date:	
			self.frame = QFrame(self)
			self.frame.setFrameShape(QFrame.Box)
			self.frame.setLineWidth(2)
			self.frame.setStyleSheet("""border: 1px solid #ccc;
										border-radius: 10px;
										border-color: yellow;								
									""")
		else:	
			self.frame = QFrame(self)
			self.frame.setFrameShape(QFrame.Box)
			self.frame.setLineWidth(2)
			self.frame.setStyleSheet("""border: 1px solid #ccc;
										border-radius: 10px;								
									""")

		# frame layout
		self.frame_layout = QVBoxLayout(self.frame)
		self.frame_layout.setContentsMargins(8, 8, 8, 8)
		self.frame_layout.setSpacing(4)

		# main layout
		main_layout = QVBoxLayout(self)
		main_layout.addWidget(self.frame)

		# adds the label and the spacer
		self.add_label()
		self.add_spacer()


	# adds spacer
	def add_spacer(self):
		self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.frame_layout.addItem(self.spacer)

	# adds label with current day and date
	def add_label(self):
		label = ClickableLabel(f"{self.day}\n{self.date}")
		label.setAlignment(Qt.AlignCenter)
		label.setStyleSheet("""padding: 4px; 
							   border: 1px solid #ccc;
					  		   border-radius: 10px;
					  		""")
		label.clicked.connect(self.label_clicked)
		self.frame_layout.addWidget(label)
	
	# opens input window if label click event
	def label_clicked(self):
		from core.window_controller import WindowController
		self.window_controller = WindowController()
		self.window_controller.start_input_window(self.day, self.date, self.frame_layout, self.spacer)
	
	def return_date_frame_widgets(self):
		return [self.date, self.frame_layout, self.spacer]
	
if __name__ == "__main__":
	pass