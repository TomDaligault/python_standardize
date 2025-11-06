from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout

from magnet_selection_widget import MagnetSelectionWidget

class StandardizePanel(QWidget):
	"""
	A domain-specific composite widget for selecting and standardizing magnets.

	This panel displays a pair of lists for selecting magnets - one for "healthy" 
	and "nonhealthy" magnets respectively - along with a button to trigger a 
	standardization action on the selected magnets.

	Each selection list is an instance of :class:`MagnetSelectionWidget`. When 
	the "Standardize" button is clicked, the provided `on_standardize` callback 
	is invoked with a dictionary of the currently selected magnets. This button
	can be targeted in QSS with the `#standardize` object name. 
	"""

	def __init__(self, healthy_magnets, nonhealthy_magnets, on_standardize):
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
		on_standardize : callable
			A callback to execute when the standardize button is
			clicked. It will be called with a single argument:
			a dictionary of all selected magnets from both lists.

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
		self.standardize_button.clicked.connect(lambda : on_standardize(self.get_selected()))

		selections_layout = QHBoxLayout()
		selections_layout.addWidget(self.nonhealthy_selector)
		selections_layout.addWidget(self.healthy_selector)

		main_layout = QVBoxLayout()
		main_layout.addLayout(selections_layout)

		main_layout.addWidget(self.standardize_button)

		self.setLayout(main_layout)

	def get_selected(self):
		"""
		Return the currently selected magnets from both selectors.

		Returns
		-------
		dict
			A merged dictionary combining the selections from both
			the healthy and non-healthy magnet lists.
		"""

		return {**self.healthy_selector.get_selected(), **self.nonhealthy_selector.get_selected()} 


