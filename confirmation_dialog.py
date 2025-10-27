from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt

class ConfirmationDialog(QDialog):
	"""
	A pre-configured QDialog with customizable text.
	"""
	def __init__(self, warning_text="Are you sure?", content_widget=None):
		super().__init__()
		self.setWindowTitle("Confirm")

		self.resize(340, 100)
		self.setModal(True)

		warning_label = QLabel(f"{warning_text}", alignment=Qt.AlignCenter)
		warning_label.setStyleSheet('color:red;')

		confirm_button = QPushButton(text="Confirm")
		confirm_button.clicked.connect(self.accept)

		cancel_button = QPushButton(text="Cancel")
		cancel_button.clicked.connect(self.reject)
		cancel_button.setDefault(True)

		button_layout = QHBoxLayout()
		button_layout.addWidget(confirm_button)
		button_layout.addWidget(cancel_button)



		main_layout = QVBoxLayout()
		main_layout.addWidget(warning_label, alignment=Qt.AlignCenter)
		if content_widget:
			main_layout.addWidget(content_widget)
		main_layout.addLayout(button_layout)

		self.setLayout(main_layout)