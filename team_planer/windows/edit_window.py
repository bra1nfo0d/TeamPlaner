import copy
import re
from PySide6.QtWidgets import (
	QWidget, QFrame, QHBoxLayout, QVBoxLayout, QPushButton,
	QSpacerItem, QSizePolicy, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut, QKeySequence
from team_planer.widgets.custom_input_bind import CustomLineEdit
from team_planer.core.storage_manager import StorageManager
from team_planer.windows.error_window import ErrorWindow

class EditWindow(QWidget):
	"""Window for editing an existing UserInput entry."""

	def __init__(
			self,
			date: str,
			text_memory: list[list[str]],
			settings: list[str],
			user_input: object,
			layout: object,
			spacer: object,
			padding: object
	):
		"""
		Args:
			date (str): Date of the input.
			text_memory (list[list[str]]): Input content to edit.
			settings (list[str]): Input content to edit.
			user_input (object): Original UserInput instance.
			layout (object): Parent layout.
			spacer (object): Parent spacer.
			padding (object): Padding layout of the input frame.
		"""
		super().__init__()
		self.storage_manager = StorageManager(self)

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

		self._setup_window()
		self._setup_layout()
		self._setup_display_frame()
		self._setup_edit_frame()
		self._setup_text_input()
		self._setup_change_button()
		self._setup_delete_button()
		self._setup_spacer()
		self._setup_shortcuts()
		self._setup_display_content()
		self._setup_edit_content()

	def _setup_window(self) -> None:
		"""Configure size, title, and always-on-top behavior."""
		self.resize(400, 400)
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		try:
			if self.text_memory[0][1].startswith("*"):
				header = self.text_memory[0][1][1:]
			else:
				header = self.text_memory[0][1]
		except IndexError:
			header = "Input Edit"
		self.setWindowTitle(f"{header} - {self.date}")

	def _setup_layout(self) -> None:
		"""Create main layout with display, edit, and input columns."""
		self.display_frame_layout = QVBoxLayout()
		self.edit_frame_layout = QVBoxLayout()
		self.row1_layout = QVBoxLayout()
		self.row2_layout = QVBoxLayout()
		self.input_layout = QVBoxLayout()
		main_layout = QHBoxLayout(self)
		main_layout.addLayout(self.row1_layout)
		main_layout.addLayout(self.row2_layout)
		main_layout.addLayout(self.input_layout)
	
	def _setup_display_frame(self) -> None:
		"""Create frame showing current input content."""
		self.display_frame = QFrame()
		self.display_frame.setLayout(self.display_frame_layout)
		self.display_frame.setStyleSheet("""
								   border: 2px solid;
								   border-radius: 10px;
								   border-color: yellow;
		""")
		self.display_frame.setFrameShape(QFrame.Box)
		self.row1_layout.addWidget(self.display_frame)

	def _setup_edit_frame(self) -> None:
		"""Create frame showing editable labels."""
		self.edit_frame = QFrame()
		self.edit_frame.setLayout(self.edit_frame_layout)
		self.edit_frame.setStyleSheet("""
								border: 2px solid;
								border-radius: 10px;
								border-color: #ccc;
								""")
		self.edit_frame.setFrameShape(QFrame.Box)
		self.row2_layout.addWidget(self.edit_frame)
	
	def _setup_text_input(self) -> None:
		"""Create text input field for editing."""
		self.text_input = CustomLineEdit()
		self.text_input.setReadOnly(True)
		self.text_input.returnPressed.connect(self._on_return)
		self.text_input.deletePressed.connect(self._on_delete)
		self.input_layout.addWidget(self.text_input)
	
	def _setup_change_button(self) -> None:
		"""Add button to apply changes."""
		change_button = QPushButton("Change")
		change_button.clicked.connect(self._change_user_input)
		self.input_layout.addWidget(change_button)
	
	def _setup_delete_button(self) -> None:
		"""Add button to delete entry."""
		delete_button = QPushButton("Delete")
		delete_button.clicked.connect(self._delete_user_input)
		self.input_layout.addWidget(delete_button)
	
	def _setup_spacer(self) -> None:
		"""Add expanding spacer for layout alignment."""
		spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.row1_layout.addItem(spacer)
		self.row2_layout.addItem(spacer)
		self.input_layout.addItem(spacer)

	def _setup_shortcuts(self) -> None:
		"""Register navigation and edit shortcuts."""
		down_shortcut = QShortcut(Qt.Key_Down, self)
		down_shortcut.activated.connect(lambda: self._change_text_focus(1))
		up_shortcut = QShortcut(Qt.Key_Up, self)
		up_shortcut.activated.connect(lambda: self._change_text_focus(-1))

		shift_up_shortcut = QShortcut(QKeySequence(Qt.SHIFT | Qt.Key_Up), self)
		shift_up_shortcut.activated.connect(self._switch_frame_focus)

		shift_down_shortcut = QShortcut(QKeySequence(Qt.SHIFT | Qt.Key_Down), self)
		shift_down_shortcut.activated.connect(self._switch_frame_focus)

		shift_return_shortcut = QShortcut(QKeySequence(Qt.SHIFT | Qt.Key_Return), self)
		shift_return_shortcut.activated.connect(self._add_text_label)

	def _delete_user_input(self) -> None:
		"""Delete input from storage and remove from UI."""
		self.storage_manager.delete_user_input(self.date, self.text_memory)
		if self.user_input.layout:
			self.user_input.layout.removeWidget(self.user_input.frame)
		self.user_input.frame.setParent(None)
		self.user_input.frame.deleteLater()
		self.close()
	
	def _change_user_input(self) -> None:
		"""Validate and apply edits to user input."""
		from team_planer.widgets.user_input import UserInput
		for i in range(len(self.text_memory)):
			if re.match(r"calc", self.text_memory[i][0]):
				for k in range(2, len(self.text_memory[i])):
					pattern = r".*#\d+(?:[,.]\d{2})?$"
					if not re.match(pattern, self.text_memory[i][k]):
						self._show_warning(error_code="E001")
						return
		self.storage_manager.delete_user_input(self.date, self.past_text_memory)
		if self.user_input.layout:
			self.user_input.layout.removeWidget(self.user_input.frame)
		self.user_input.frame.setParent(None)
		self.user_input.frame.deleteLater()
		self.padding.deleteLater()
		changed_user_input = UserInput(
			self.date,
			self.text_memory,
			self.settings,
			self.layout,
			self.spacer
		)
		changed_user_input._show_input()
		self.storage_manager.store_user_input(self.date, self.text_memory, self.settings)
		self.close()

	def _setup_display_content(self) -> None:
		"""Fill display frame with formatted labels."""
		for i in range(len(self.text_memory)):
			label = QLabel()
			self.label_memory.append(label)
			self.display_frame_layout.addWidget(label)			
			if re.match(r"calc", self.text_memory[i][0]):
				text = self.text_memory[i][1][1:]
				for j in range(2, len(self.text_memory[i])):
					text_num = self.text_memory[i][j].split("#")
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
				color = "yellow"
			else:
				color = "#ccc"				
			label.setStyleSheet(f"""
					   border: 2px solid;
					   border-radius: 10px;
					   border-color: {color};
					   """)
			label.setAlignment(Qt.AlignCenter)
			label.setContentsMargins(5, 2, 5, 2)
	
	def _delete_cur_input_view(self) -> None:
		"""Rebuild display labels."""
		for label in self.label_memory:
			label.deleteLater()
		self.label_memory = []
		self._setup_display_content()
	
	def _setup_edit_content(self) -> None:
		"""Fill edit frame with editable labels."""
		for i in range(1, len(self.text_memory[self.text_focus])):
			label = QLabel()
			text = self.text_memory[self.text_focus][i]
			if text.startswith("*"):
				text = text[1:]
			label.setText(text)
			self.edit_label_memory.append(label)
			self.edit_frame_layout.addWidget(label)
			if i == self.edit_focus+1:
				color = "yellow"
			else:
				color = "#ccc"
			label.setStyleSheet(f"""
					   border: 2px solid;
					   border-radius: 10px;
					   border-color: {color};
					   """)
			label.setAlignment(Qt.AlignCenter)
			label.setContentsMargins(5, 2, 5, 2)

	def _delete_cur_edit_view(self) -> None:
		"""Rebuild editable labels."""
		self.storage_manager.delete_user_input(self.date, self.past_text_memory)
		for label in self.edit_label_memory:
			label.deleteLater()		
		self.edit_label_memory = []
		self._setup_edit_content()

	def _change_text_focus(self, val: int) -> None:
		"""Move text or label selection focus."""
		if self.frame_focus == 0:
			cur_label = self.label_memory[self.text_focus]
			cur_label.setStyleSheet("""
						   border: 2px solid;
						   border-radius: 10px;
						   border-color: #ccc;
						   """)
			self.text_focus = (self.text_focus+val) % len(self.text_memory)
			new_label = self.label_memory[self.text_focus]
			new_label.setStyleSheet("""
						   border: 2px solid;
						   border-radius: 10px;
						   border-color: yellow;
						   """)
			self._delete_cur_edit_view()
			self.edit_focus = 0
		else:
			cur_label = self.edit_label_memory[self.edit_focus]
			cur_label.setStyleSheet("""
						   border: 2px solid;
						   border-radius: 10px;
						   border-color: #ccc;
						   """)
			self.edit_focus = (self.edit_focus+val) % len(self.edit_label_memory)
			new_label = self.edit_label_memory[self.edit_focus]
			new_label.setStyleSheet("""
						   border: 2px solid;
						   border-radius: 10px;
						   border-color: yellow;
						   """)
			new_text = self.text_memory[self.text_focus][self.edit_focus+1]
			if new_text.startswith("*"):
				self.text_input.setReadOnly(True)
				self.text_input.setText("")
			else:
				self.text_input.setReadOnly(False)
				self.text_input.setText(self.text_memory[self.text_focus][self.edit_focus+1])

	def _switch_frame_focus(self) -> None:
		"""Toggle focus between display and edit frame."""
		self.frame_focus = (self.frame_focus+1)%2
		if self.frame_focus == 0:
			self.display_frame.setStyleSheet("""
									border: 2px solid;
									border-radius: 10px;
									border-color: yellow;
									""")
			self.edit_frame.setStyleSheet("""
								 border: 2px solid;
								 border-radius: 10px;
								 border-color: #ccc;
								 """)
			self.text_input.setText("")
		else:
			self.display_frame.setStyleSheet("""
									border: 2px solid;
									border-radius: 10px;
									border-color: #ccc;
									""")
			self.edit_frame.setStyleSheet("""
								 border: 2px solid;
								 border-radius: 10px;
								 border-color: yellow;
								 """)
			focus_label = self.edit_label_memory[0]
			focus_label.setStyleSheet("""
							 border: 2px solid;
							 border-radius: 10px;
							 border-color: yellow;
							 """)
			focus_text = self.text_memory[self.text_focus][1]
			if focus_text.startswith("*"):
				self.text_input.setReadOnly(True)
				self.text_input.setText("")
			else:
				self.text_input.setReadOnly(False)
				self.text_input.setText(self.text_memory[self.text_focus][self.edit_focus+1])
	
	def _on_delete(self) -> None:
		"""Delete current editable label (except headers)."""
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
								 border: 2px solid;
								 border-radius: 10px;
								 border-color: yellow;
								 """)
			text = self.text_memory[self.text_focus][self.edit_focus+1]
			if text.startswith("*"):
				self.text_input.setReadOnly(True)
				self.text_input.setText("")
			else:
				self.text_input.setReadOnly(False)
				self.text_input.setText(text)
			self._delete_cur_input_view()

	def _on_return(self) -> None:
		"""Update focused label text form input."""
		if self.frame_focus == 1 and not self.text_memory[self.text_focus][self.edit_focus+1].startswith("*"):
			label = self.edit_label_memory[self.edit_focus]
			text = self.text_input.text()
			if text.startswith("*"):
				self._show_warning(error_code="E002")
				return
			if re.match(r"calc", self.text_memory[self.text_focus][0]) and not re.match(r".*#\d+(?:[,.]\d{2})?$", text):
				self._show_warning(error_code="E001")
				return
			label.setText(text)
			self.text_memory[self.text_focus][self.edit_focus+1] = text
			self._delete_cur_input_view()

	def _add_text_label(self) -> None:
		"""Add new text label below current edit label."""
		if self.frame_focus == 1:
			self.text_memory[self.text_focus].insert(self.edit_focus+2, "")
			self.edit_focus = self.edit_focus+1
			self._delete_cur_edit_view()
			self.text_input.setReadOnly(False)
			self.text_input.setText("")

	def _show_warning(self, error_code: str) -> None:
		"""
		Show error popup.

		Args:
			error_code (str): Error identifier (e.g., 'E001').
		"""
		error_window = ErrorWindow(error_code, self)
		error_window.exec()

	def closeEvent(self, event) -> None:
		"""Clean up on close."""
		del self
		event.accept()


if __name__ == "__main__":
	pass