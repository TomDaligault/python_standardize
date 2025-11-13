from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

from magnet_selection_widget import MagnetSelectionWidget

class StandardizePanel(QWidget):
	"""
	A domain-specific composite widget for selecting magnets for standardization.

	This panel displays a pair of lists for selecting magnets - one for "healthy" 
	and "nonhealthy" magnets respectively - along with a button that, on click,
	emits a signal containing all currently selected magnets. 

	Each selection list is an instance of :class:`MagnetSelectionWidget`.The 
	button can be targeted in QSS with the `#standardize_button` object name. 

	Attributes
	----------
	standardize_requested : pyqtSignal(dict)
		Emitted when the user clicks the "Standardize" button. The signal carries a 
		dictionary mapping all currently selected magnet names to their status messages.
	"""
	standardize_requested = pyqtSignal(dict)

	def __init__(self, healthy_magnets, nonhealthy_magnets):
		"""
		Initialize the standardize panel.

		Parameters
		----------
		healthly_magnets : dict[str, str]
			A mapping of healthy magnet names to their status values.
			All healthy magnets are pre-selected by default.
		nonhealthly_magnets : dict[str, str]
			A mapping of non-healthy magnet names to their status values.
			None are pre-selected by default.
		"""

		super().__init__()

		self.healthy_selector = MagnetSelectionWidget(label_text='healthy magnets')
		self.nonhealthy_selector = MagnetSelectionWidget(label_text='non-healthy magnets')

		self.healthy_selector.set_magnets(healthy_magnets, check_all=True)
		self.healthy_selector.setMinimumWidth(350)

		self.nonhealthy_selector.set_magnets(nonhealthy_magnets)
		self.nonhealthy_selector.setMinimumWidth(350)

		self.standardize_button = QPushButton(text='Standardize')
		self.standardize_button.setObjectName('standardize_button')
		self.standardize_button.clicked.connect(self._emit_standardize_request)

		selections_layout = QHBoxLayout()
		selections_layout.addWidget(self.nonhealthy_selector)
		selections_layout.addWidget(self.healthy_selector)

		main_layout = QVBoxLayout()
		main_layout.addLayout(selections_layout)

		main_layout.addWidget(self.standardize_button)

		self.setLayout(main_layout)

	def _emit_standardize_request(self):
		"""
		Emit the :attr:`standardize_requested` signal with the currently selected magnets.

		The emitted dictionary maps each selected magnet name to its corresponding 
		status message.
		"""
		
		selected = {**self.healthy_selector.get_selected(), **self.nonhealthy_selector.get_selected()}
		self.standardize_requested.emit(selected)

