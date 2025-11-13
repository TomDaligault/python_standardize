from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt

class ConfirmationDialog(QDialog):
	"""
	A pre-configured QDialog with customizable text.
	"""
	def __init__(self, parent=None, warning_text="Are you sure?"):
		"""
		Initialize the dialog.

		Parameters
		----------
		parent : QWidget, optional
			The parent for the dialog. If provided, the dialog will
			inherit styling and be centered realtive to the parent.
		warning_text : str
			The warning message displayed in the dialog.
		"""
		super().__init__(parent=parent)
		self.setWindowTitle("Are you sure?")

		self.setMinimumSize(350, 120)
		self.setModal(True)

		warning_label = QLabel(f"{warning_text}", alignment=Qt.AlignCenter)
		warning_label.setStyleSheet('color: #d94a4a;')

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
		main_layout.addLayout(button_layout)

		self.setLayout(main_layout)