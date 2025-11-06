from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QScrollArea, QLabel
from PyQt5.QtCore import Qt

class MagnetSelectionWidget(QWidget):
	"""
	A domain-specific scrollable list of checkboxes for selecting magnets to standardize.

	This widget displays a vertical list of checkboxes inside a scroll area,
	one for each magnet name–status pair. The selection state is tracked
	internally and can be retrieved via `get_selected`. The widget can be 
	targeted in QSS with the object name #selection.
	"""

	def __init__(self, label_text=None):
		"""
		Initialize the magnet selection widget.

		Parameters
		----------
		label_text : str, optional
			An optional label to display above the scroll area.
		"""

		super().__init__()
		self._selected = {}

		checkboxes_widget = QWidget()
		checkboxes_widget.setObjectName('selection')
		self.checkboxes_layout = QVBoxLayout(checkboxes_widget)

		scroll_area = QScrollArea()
		scroll_area.setWidgetResizable(True)
		scroll_area.setWidget(checkboxes_widget)
		scroll_area.setFocusPolicy(Qt.NoFocus)

		main_layout = QVBoxLayout()
		if label_text is not None:
			label = QLabel(label_text)
			main_layout.addWidget(label, alignment=Qt.AlignCenter)
		main_layout.addWidget(scroll_area)

		self.setLayout(main_layout)

	def set_magnets(self, magnets, check_all=False):
		"""
		Populate the list of checkboxes from a dictionary of magnets.

		Parameters
		----------
		magnets : dict[str, str]
			A mapping of magnet names to their status messages.
		check_all : bool, optional
			If True, all checkboxes are initially checked.

		Notes
		-----
		Calling this method replaces any existing checkboxes and resets
		the internal selection state.
		"""

		self.clear_magnets()
		for name, status in magnets.items():
			checkbox = QCheckBox(f"{name} - {status}")
			checkbox.stateChanged.connect(lambda state, m=name, s=status: self._on_state_changed(state, m, s))

			if check_all:
				checkbox.setChecked(True)
				
			self.checkboxes_layout.addWidget(checkbox)
		self.checkboxes_layout.addStretch()

	def clear_magnets(self):
		"""
		Remove all widgets from the checkbox layout and clear the selected state.
		"""

		while self.checkboxes_layout.count():
			layout_item = self.checkboxes_layout.takeAt(0)
			widget = layout_item.widget() 
			if widget is not None:
				widget.deleteLater()
		self._selected.clear()


	def _on_state_changed(self, state, name, status):
		"""
		Update internal selected state when a checkbox is toggled.

		Parameters
		----------
		state : Qt.CheckState
			The new check state of the checkbox.
		name : str
			The name of the magnet associated with this checkbox.
		status : str
			The current status string for the magnet.
		"""
		if state == Qt.Checked:
			self._selected[name] = status
		else:
			self._selected.pop(name, None)

	def get_selected(self):
		"""
		Return the currently selected magnets as a dictionary of names and statuses.

		Returns
		-------
		dict[str, str]
			A mapping of magnet names to their statuses for all currently checked checkboxes.
		"""

		return dict(self._selected)

