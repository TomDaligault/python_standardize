from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt

class ConfirmDialog(QDialog):
	"""
	A pre-configured QDialog with customizable text.
	"""
	def __init__(self, warning_text="Are you sure?"):
		super().__init__()
		self.setWindowTitle("Confirm")
		self.setModal(True)

		warning_label = QLabel(f"<span style='color: red;'>{warning_text}</span>", alignment=Qt.AlignCenter)
		confirm_button = QPushButton(text="Confirm")
		cancel_button = QPushButton(text="Cancel")
		cancel_button.setAutoDefault(True)

		confirm_button.clicked.connect(self.accept)
		cancel_button.clicked.connect(self.reject)

		button_layout = QHBoxLayout()
		button_layout.addWidget(confirm_button)
		button_layout.addWidget(cancel_button)

		layout = QVBoxLayout()
		layout.addWidget(warning_label, alignment=Qt.AlignCenter)
		layout.addLayout(button_layout)

		self.setLayout(layout)