from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QScrollArea, QFrame
from PyQt5.QtCore import Qt

class MagnetSelectionWidget(QWidget):
	"""
	A scrollable list of checkboxes for selecting magnets to standardize.
	"""

	def __init__(self, names_and_statuses):
		super().__init__()
		self._selected = {}

		# Create the container widget that will hold all checkboxes
		content_widget = QWidget()
		content_layout = QVBoxLayout(content_widget)
		content_widget.setStyleSheet("padding :0px")
		
		for name, status in names_and_statuses.items():
			checkbox = QCheckBox(f"{name} — {status}")
			checkbox.stateChanged.connect(lambda state, m=name, s=status: self._on_state_changed(state, m, s))
			checkbox.setStyleSheet('background-color: #FFAF00')
			content_layout.addWidget(checkbox)

		# Add stretch so last checkbox doesn’t glue to the bottom
		content_layout.addStretch()

		# Wrap in a scroll area
		scroll = QScrollArea()
		scroll.setWidgetResizable(True)
		scroll.setWidget(content_widget)
		# scroll.setFrameShape(QFrame.NoFrame)  # cleaner look, optional

		# Main layout for this widget
		main_layout = QVBoxLayout(self)
		main_layout.addWidget(scroll)

	def _on_state_changed(self, state, name, status):
		if state == Qt.Checked:
			self._selected[name] = f"{status} (overridden)"
		else:
			self._selected.pop(name, None)

	def get_selected(self):
		return self._selected
