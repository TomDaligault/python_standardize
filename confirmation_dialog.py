from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt

class ConfirmDialog(QDialog):
	def __init__(self, warning_text="Are you sure?"):
		super().__init__()
		self.setWindowTitle("Confirm")
		self.setModal(True)  # Make it modal

		warning_label = QLabel(f"<span style='color: red;'>{warning_text}</span>", alignment=Qt.AlignCenter)
		confirm_button = QPushButton(text="Confirm")
		cancel_button = QPushButton(text="Cancel")
		cancel_button.setAutoDefault(True)


		confirm_button.clicked.connect(self.accept)  # Built-in QDialog method
		cancel_button.clicked.connect(self.reject)

		# Layout for buttons
		button_layout = QHBoxLayout()
		button_layout.addWidget(confirm_button)
		button_layout.addWidget(cancel_button)

		# Main layout
		layout = QVBoxLayout()
		layout.addWidget(warning_label, alignment=Qt.AlignCenter)
		layout.addLayout(button_layout)

		self.setLayout(layout)