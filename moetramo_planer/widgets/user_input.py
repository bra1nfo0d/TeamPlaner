import re
from PySide6.QtWidgets import QLabel, QFrame, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from widgets.clickable_label import ClickableLabel
from widgets.clickable_frame import ClickableFrame
from core.config_manager import ConfigManager
from windows.edit_window import EditWindow


class UserInput:
	def __init__(self, text_memory=None, layout=None, spacer=None, date=None, settings=False):
		config_manager = ConfigManager()


		self.layout = layout
		self.spacer = spacer
		self.setting = settings
		self.date = date
		self.text_memory = text_memory
		label_memory = []
		inner_border_color = settings[2]
		outer_border_color = settings[3]
		calc = 0
		calc_true_color = config_manager.load_config()["calc_true_color"]
		calc_false_color = config_manager.load_config()["calc_false_color"]

		self.frame = ClickableFrame()
		self.frame_layout = QVBoxLayout(self.frame)
		self.frame.clicked.connect(lambda: self.click())

		for i in range(len(text_memory)):
			label = QLabel()
			label_memory.append(label)
			self.frame_layout.addWidget(label)
			for j in range(1, len(text_memory[i])):
				if text_memory[i][j].startswith("*"):
					add_text = text_memory[i][j][1:]
				else:
					add_text = text_memory[i][j]
				cur_text = label.text()
				if re.match(r"text$", text_memory[i][0]):
					if j == 1:
						label.setText(add_text)
					else:
						label.setText(cur_text + "\n" + add_text)
				elif re.match(r"calc#", text_memory[i][0]):
					goal = int(text_memory[i][0].split("#")[1])
					if j == 1:
						label.setText(add_text)
					else:
						text_num = text_memory[i][j].split("#")
						add_text = text_num[0]
						str_num = text_num[1]
						if "," in str_num:
							str_num = str_num.replace(",", ".")
						num = float(str_num)
						label.setText(cur_text + "\n" + add_text)
						calc += num
				label.setAlignment(Qt.AlignCenter)
					
		if calc > 0 and calc >= goal:
			self.frame.setStyleSheet(f"border: 2px solid {calc_true_color};")
		elif calc > 0 and calc < goal:
			self.frame.setStyleSheet(f"border: 2px solid {calc_false_color};")
		else:
			self.frame.setStyleSheet(f"border: 2px solid {outer_border_color};")
		for label in label_memory:
			label.setStyleSheet(f"border: 2px solid {inner_border_color};")

	def show_input(self):
		self.padding_layout = QVBoxLayout()
		self.padding_layout.setContentsMargins(0, 0, 0, 5)
		spacer = self.spacer
		self.layout.removeItem(self.spacer)
		self.padding_layout.addWidget(self.frame)
		self.layout.addLayout(self.padding_layout)
		self.layout.addItem(spacer)

	def click(self):	
		self.edit_window = EditWindow(
			date=self.date,
			text_memory=self.text_memory,
			settings=self.setting,
			user_input=self,
			layout=self.layout,
			spacer=self.spacer,
			padding=self.padding_layout)		
		self.edit_window.show()

if __name__ == "__main__":
	pass