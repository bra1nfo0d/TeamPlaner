from PySide6.QtCore import QObject, QTimer, Signal

class TimeManager(QObject):
	signal = Signal()

	def __init__(self, interval_ms: int=60000, parent=None):
		super().__init__(parent)

		self.timer = QTimer()
		self.timer.timeout.connect(self._send_signal)
		self.timer.start(interval_ms)

	def _send_signal(self):
		self.signal.emit()