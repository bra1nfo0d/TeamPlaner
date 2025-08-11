from windows.input_window import InputWindow

class EditWindow(InputWindow):
	def __init__(self, day, date, target_frame, target_spacer):
		super().__init__(day, date, target_frame, target_spacer)
		# in progress