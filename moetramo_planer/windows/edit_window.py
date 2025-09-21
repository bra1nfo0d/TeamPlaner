import copy
import re
from PySide6.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QLabel, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut, QKeySequence
from widgets.custom_input_bind import CustomLineEdit
from core.storage_manager import StorageManager

class EditWindow(QWidget):
	def __init__(self, date, text_memory, settings, user_input, layout, spacer, padding):
		super().__init__()
		
		print(text_memory)
		
		self.storage_manager = StorageManager()

		self.user_input = user_input
		self.date = date
		self.text_memory = text_memory
		self.past_text_memory = copy.deepcopy(text_memory)
		self.settings = settings
		self.layout = layout
		self.spacer = spacer
		self.padding = padding

		self.text_focus = 0
		self.frame_focus = 0
		self.edit_focus = 0

		self.label_memory = []
		self.edit_label_memory = []

		self.resize(400, 400)

		self.setWindowFlags(Qt.WindowStaysOnTopHint)

		try:
			if self.text_memory[0][1].startswith("*"):
				header = self.text_memory[0][1][1:]
			else:
				header = self.text_memory[0][1]
		except IndexError:
			header = "Bearbeitung"
		self.setWindowTitle(f"{header} - {date}")

		self.display_frame = QFrame()
		self.display_frame.setStyleSheet("""
								border: 2px solid #ccc;
								border-radius: 10px""")
		self.display_frame.setFrameShape(QFrame.Box)
		
		self.edit_frame = QFrame()
		self.edit_frame.setStyleSheet("""
								border: 2px solid #ccc;
								border-radius: 10px;""")
		self.edit_frame.setFrameShape(QFrame.Box)
		
		self.text_input = CustomLineEdit()
		self.text_input.setReadOnly(True)
		self.text_input.returnPressed.connect(self.on_return)
		self.text_input.deletePressed.connect(self.on_delete)

		change_button = QPushButton("Change")
		change_button.clicked.connect(self.change_user_input)
		
		delete_button = QPushButton("Delete")
		delete_button.clicked.connect(self.delete_user_input)

		spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

		self.display_frame_layout = QVBoxLayout(self.display_frame)
		self.display_frame.setStyleSheet("""
					   border: 2px solid yellow;
					   border-radius: 10px""")

		self.edit_frame_layout = QVBoxLayout(self.edit_frame)
		
		row1_layout = QVBoxLayout()
		row1_layout.addWidget(self.display_frame)
		row1_layout.addItem(spacer)
		row2_layout = QVBoxLayout()
		row2_layout.addWidget(self.edit_frame)
		row2_layout.addItem(spacer)
		input_layout = QVBoxLayout()

		input_layout.addWidget(self.text_input)
		input_layout.addWidget(change_button)
		input_layout.addWidget(delete_button)
		input_layout.addItem(spacer)

		main_layout = QHBoxLayout(self)
		main_layout.addLayout(row1_layout)
		main_layout.addLayout(row2_layout)
		main_layout.addLayout(input_layout)

		down_shortcut = QShortcut(Qt.Key_Down, self)
		down_shortcut.activated.connect(lambda: self.change_text_focus(0))
		up_shortcut = QShortcut(Qt.Key_Up, self)
		up_shortcut.activated.connect(lambda: self.change_text_focus(1))
		shift_up_shortcut = QShortcut(QKeySequence(Qt.SHIFT | Qt.Key_Up), self)
		shift_up_shortcut.activated.connect(self.switch_frame_focus)
		shift_down_shortcut = QShortcut(QKeySequence(Qt.SHIFT | Qt.Key_Down), self)
		shift_down_shortcut.activated.connect(self.switch_frame_focus)
		shift_return_shortcut = QShortcut(QKeySequence(Qt.SHIFT | Qt.Key_Return), self)
		shift_return_shortcut.activated.connect(self.add_text_label)

		self.create_input_view()
		self.create_edit_view()

	def delete_user_input(self):
		self.storage_manager.delete_user_input(
			text_memory=self.text_memory,
			date=self.date)
		if self.user_input.layout:
			self.user_input.layout.removeWidget(self.user_input.frame)
		self.user_input.frame.setParent(None)
		self.user_input.frame.deleteLater()
		self.close()
	
	def change_user_input(self):
		from widgets.user_input import UserInput

		for i in range(len(self.text_memory)):
			if re.match(r"calc", self.text_memory[i][0]):
				for k in range(2, len(self.text_memory[i])):
					pattern = r".*#\d+(?:[,.]\d{2})?$"
					if not re.match(pattern, self.text_memory[i][k]):
						self.show_warning(error_code=1)
						return

		self.storage_manager.delete_user_input(
			text_memory=self.past_text_memory,
			date=self.date)
		if self.user_input.layout:
			self.user_input.layout.removeWidget(self.user_input.frame)
		self.user_input.frame.setParent(None)
		self.user_input.frame.deleteLater()
		self.padding.deleteLater()
		changed_user_input = UserInput(
			layout=self.layout,
			text_memory=self.text_memory,
			spacer=self.spacer,
			settings=self.settings,
			date=self.date)
		changed_user_input.show_input()
		self.storage_manager.store_user_input(
			text_memory=self.text_memory,
			date=self.date,
			settings=self.settings)
		self.close()

	def create_input_view(self):
		for i in range(len(self.text_memory)):
			label = QLabel()
			self.label_memory.append(label)
			self.display_frame_layout.addWidget(label)
			
			if re.match(r"calc", self.text_memory[i][0]):
				text = self.text_memory[i][1][1:]
				for j in range(2, len(self.text_memory[i])):
					text_num = self.text_memory[i][j].split("#")
					print(text_num)
					text_snipped = text_num[0]
					num_snipped = text_num[1]

					if "," in num_snipped:
						num_snipped = num_snipped + "€"
					elif "." in num_snipped:
						num_snipped = num_snipped.replace(".", ",")
						num_snipped = num_snipped + "€"
					else:
						num_snipped = num_snipped + ",00€"
					text = text + "\n" + text_snipped + " -> " + num_snipped
				label.setText(text)
			else:
				text = "\n".join(self.text_memory[i][1:])
				if text.startswith("*"):
					text = text[1:]
				label.setText(text)
			if i == self.text_focus:
				label.setStyleSheet("""
						border: 2px solid yellow;
						border-radius: 10px""")
			else:
				label.setStyleSheet("""
						border: 2px solid #ccc;
						border-radius: 10px;""")
			label.setAlignment(Qt.AlignCenter)
			label.setContentsMargins(5, 2, 5, 2)
	
	def delete_cur_input_view(self):
		for label in self.label_memory:
			label.deleteLater()
		self.label_memory = []
		self.create_input_view()
	
	def create_edit_view(self):
		for i in range(1, len(self.text_memory[self.text_focus])):
			label = QLabel()
			text = self.text_memory[self.text_focus][i]
			if text.startswith("*"):
				text = text[1:]
			label.setText(text)
			self.edit_label_memory.append(label)
			self.edit_frame_layout.addWidget(label)
			if i == self.edit_focus+1:
				label.setStyleSheet("""
							border: 2px solid yellow;
							border-radius: 10px;""")
			else:
				label.setStyleSheet("""
							border: 2px solid #ccc;
							border-radius: 10px;""")
			label.setAlignment(Qt.AlignCenter)
			label.setContentsMargins(5, 2, 5, 2)

	def delete_cur_edit_view(self):
		for label in self.edit_label_memory:
			label.deleteLater()		
		self.edit_label_memory = []
		self.create_edit_view()

	def change_text_focus(self, val):
		if val == 0:
			x = 1
		elif val == 1:
			x = -1
		if self.frame_focus == 0:
			cur_label = self.label_memory[self.text_focus]
			cur_label.setStyleSheet("""
							border: 2px solid #ccc;
							border-radius: 10px;""")
			self.text_focus = (self.text_focus+x) % len(self.text_memory)
			new_label = self.label_memory[self.text_focus]
			new_label.setStyleSheet("""
							border: 2px solid yellow;
						   	border-radius: 10px;""")
			self.delete_cur_edit_view()
			self.edit_focus = 0
		else:
			cur_label = self.edit_label_memory[self.edit_focus]
			cur_label.setStyleSheet("""
							border: 2px solid #ccc;
						   	border-radius: 10px;""")
			self.edit_focus = (self.edit_focus+x) % len(self.edit_label_memory)
			new_label = self.edit_label_memory[self.edit_focus]
			new_label.setStyleSheet("""
							border: 2px solid yellow;
						   	border-radius: 10px;""")
			new_text = self.text_memory[self.text_focus][self.edit_focus+1]
			print(new_text)
			if new_text.startswith("*"):
#				self.text_input.setEnabled(False)
				self.text_input.setReadOnly(True)
				self.text_input.setText("")
			else:
#				self.text_input.setEnabled(True)
				self.text_input.setReadOnly(False)
				self.text_input.setText(self.text_memory[self.text_focus][self.edit_focus+1])

	def switch_frame_focus(self):
		self.frame_focus = (self.frame_focus+1)%2
		if self.frame_focus == 0:
			self.display_frame.setStyleSheet("""
									border: 2px solid yellow;
									border-radius: 10px;""")
			self.edit_frame.setStyleSheet("""
								 border: 2px solid #ccc;
								 border-radius: 10px;""")
			self.text_input.setText("")
		else:
			self.display_frame.setStyleSheet("""
									border: 2px solid #ccc;
									border-radius: 10px;""")
			self.edit_frame.setStyleSheet("""
								 border: 2px solid yellow;
								 border-radius: 10px;""")
			focus_label = self.edit_label_memory[0]
			focus_label.setStyleSheet("""
								border: 2px solid yellow;
							 	border-radius: 10px;""")
			focus_text = self.text_memory[self.text_focus][1]
			print(focus_text)
			if focus_text.startswith("*"):
#				self.text_input.setEnabled(False)
				self.text_input.setReadOnly(True)
				self.text_input.setText("")
			else:
#				self.text_input.setEnabled(True)
				self.text_input.setReadOnly(False)
				self.text_input.setText(self.text_memory[self.text_focus][self.edit_focus+1])


	# Disable fix header delete		
	def on_delete(self):
		if self.frame_focus == 1 and len(self.edit_label_memory) > 1:
			label = self.edit_label_memory[self.edit_focus]
			del_text = self.text_memory[self.text_focus][self.edit_focus+1]
			if del_text.startswith("*"):
				return
			self.edit_label_memory.remove(label)
			self.text_memory[self.text_focus].remove(del_text)
			label.deleteLater()

			if self.edit_focus+1 > len(self.edit_label_memory):
				self.edit_focus -= 1

			new_focus_label = self.edit_label_memory[self.edit_focus]
			new_focus_label.setStyleSheet("""
								border: 2px solid yellow;
								border-radius: 10px;""")
			text = self.text_memory[self.text_focus][self.edit_focus+1]
#			text = new_focus_label.text()
			if text.startswith("*"):
				self.text_input.setReadOnly(True)
				self.text_input.setText("")
			else:
				self.text_input.setReadOnly(False)
				self.text_input.setText(text)
			self.delete_cur_input_view()


	def on_return(self):
		if self.frame_focus == 1 and not self.text_memory[self.text_focus][self.edit_focus+1].startswith("*"):
			label = self.edit_label_memory[self.edit_focus]
			text = self.text_input.text()
			if text.startswith("*"):
				self.show_warning(error_code=2)
				return
			if re.match(r"calc", self.text_memory[self.text_focus][0]) and not re.match(r".*#\d+(?:[,.]\d{2})?$", text):
				self.show_warning(error_code=1)
			label.setText(text)
			self.text_memory[self.text_focus][self.edit_focus+1] = text
			self.delete_cur_input_view()

	def add_text_label(self):
		if self.frame_focus == 1:
			self.text_memory[self.text_focus].insert(self.edit_focus+2, "")
			self.edit_focus = self.edit_focus+1
			self.delete_cur_edit_view()
			self.text_input.setReadOnly(False)
			self.text_input.setText("")

	
	def show_warning(self, error_code):
		if error_code == 1:
			error_text = "Eine Calculation ist Falsch Eingegeben.\nDie Eingabe in ein Calculationsfeld muss folgende Form haben\n\"Text\"#\"Betrag\""
		elif error_code == 2:
			error_text = "Die Eingabe darf nicht mit einem * Beginnnen."
		msg = QMessageBox()
		msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
		msg.setIcon(QMessageBox.Warning)
		msg.setWindowTitle("Eingabe Fehler!")
		msg.setText(error_text)
		msg.setStandardButtons(QMessageBox.Ok)
		msg.exec()

	def closeEvent(self, event):
		del self
		event.accept()