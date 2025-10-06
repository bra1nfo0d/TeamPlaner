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
	"""
	A window that allows editing of an existing UserInput entry.

	Provider:
		- A display frame showing the original content.
		- An editable frame showing individual text/calculation items.
		- Shortcuts for navigating between inputs and frames.
		- Buttons to change, delete, or update entries.
		- Validation and error handling.

	Attributs:
		storage_manager (StorageManager): Handles persistent input storage.
		user_input (object): Reference to the original UserInput object.
		date (str): Date associated with the input being edited.
		text_memory (list[list[str]]): Current editable copy of the input content.
		past_text_memory (list[list[str]]): Deep copy of the original input for reference.
		settings (list[str]): Configuration values for this input.
		layout (object): Layout of the parent container holding this input.
		spacer (object): Spacer used in the parent layout.
		padding (object): Padding layout for this input’s frame.
		text_focus (int): Index of the currently focused input group.
		frame_focus (int): Indicates which frame is active (0=display, 1=edit).
		edit_focus (int): Index of the currently focused label in edit mode.
		label_memory (list[QLabel]): Labels used in the display frame.
		edit_label_memory (list[QLabel]): Labels used in the editable frame.
	"""

	def __init__(self,
			  date: str,
			  text_memory: list[list[str]],
			  settings: list[str],
			  user_input: object,
			  layout: object,
			  spacer: object,
			  padding: object):
		"""
		Initialize the edit window.

		Args:
			date (str): Date associated with this input.
			text_memory (list[list[str]]): Input content to edit.
			settings (list[str]): Input configuration.
			user_input (object): Original UserInput instance being edited.
			layout (object): Parent layout containing the input.
			spacer (object): Spacer item in the parent layout.
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
		"""
		Configure window size, title, and always-on-top behavior.
		"""
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
		"""
		Create the main layout with display, edit, and input columns.
		"""
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
		"""
		Create the display frame showing the current input content.
		"""
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
		"""
		Create the editable frame showing detailed labels of the input.
		"""
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
		"""
		Create a read-only input field for editing entries.
		"""
		self.text_input = CustomLineEdit()
		self.text_input.setReadOnly(True)
		self.text_input.returnPressed.connect(self._on_return)
		self.text_input.deletePressed.connect(self._on_delete)
		self.input_layout.addWidget(self.text_input)
	
	def _setup_change_button(self) -> None:
		"""
		Create a button to confirm and apply changes to the input.
		"""
		change_button = QPushButton("Change")
		change_button.clicked.connect(self._change_user_input)
		self.input_layout.addWidget(change_button)
	
	def _setup_delete_button(self) -> None:
		"""
		Create a button to delete the current input entirely.
		"""
		delete_button = QPushButton("Delete")
		delete_button.clicked.connect(self._delete_user_input)
		self.input_layout.addWidget(delete_button)
	
	def _setup_spacer(self) -> None:
		"""
		Add expanding spacers for proper layout alignment.
		"""
		spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.row1_layout.addItem(spacer)
		self.row2_layout.addItem(spacer)
		self.input_layout.addItem(spacer)

	def _setup_shortcuts(self) -> None:
		"""
		Register navigation and edit keyboard shortcuts.
		"""
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
		"""
		Permanently delete this input from storage and the UI.
		Removes the corresponding frame and closes the edit window.
		"""	
		self.storage_manager.delete_user_input(self.date, self.text_memory)
		if self.user_input.layout:
			self.user_input.layout.removeWidget(self.user_input.frame)
		self.user_input.frame.setParent(None)
		self.user_input.frame.deleteLater()
		self.close()
	
	def _change_user_input(self) -> None:
		"""
		Validate and apply changes to the input.

		- Validates calc entries against the expected format.
		- Replaces the old UserInput with an updated one.
		- Updates persistent storage.
		"""
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
		"""
		Populate the display frame with formatted labels
		showing the current text or calculation entries.
		"""
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
		"""
		Clear and rebuild the display content labels.
		"""
		for label in self.label_memory:
			label.deleteLater()
		self.label_memory = []
		self._setup_display_content()
	
	def _setup_edit_content(self) -> None:
		"""
		Populate the edit frame with editable labels for the focused entry.
		"""
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
		"""
		Clear and rebuild the editable content labels.
		"""
		self.storage_manager.delete_user_input(self.date, self.past_text_memory)
		for label in self.edit_label_memory:
			label.deleteLater()		
		self.edit_label_memory = []
		self._setup_edit_content()

	def _change_text_focus(self, val: int) -> None:
		"""
		Change the focus to another entry label.

		Args:
			val (int): +1 for next entry, -1 for previous entry.
		"""
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
		"""
		Toggle between focusing the display frame and the edit frame.
		"""
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

	#TODO: Disable fix header delete	
	def _on_delete(self) -> None:
		"""
		Handle delete key press in edit mode.

		Removes the currently focused label (unless it's a fixed header).
		"""
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
		"""
		Handle return/enter key press in edit mode.

		Updates the currently focused entry with new text from the input field.
		"""
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
		"""
		Add a new empty text label below the current one in edit mode.
		"""
		if self.frame_focus == 1:
			self.text_memory[self.text_focus].insert(self.edit_focus+2, "")
			self.edit_focus = self.edit_focus+1
			self._delete_cur_edit_view()
			self.text_input.setReadOnly(False)
			self.text_input.setText("")

	def _show_warning(self, error_code: str) -> None:
		"""
		Show an error popup with the given code.

		Args:
			error_code (str): Error identifier (e.g., 'E001').
		"""
		error_window = ErrorWindow(error_code, self)
		error_window.exec()

	def closeEvent(self, event) -> None:
		"""
		Cleanup on close and accept the close event.
		"""
		del self
		event.accept()


if __name__ == "__main__":
	pass