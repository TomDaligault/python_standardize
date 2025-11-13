from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

from .standardize_panel import StandardizePanel
from .tab_widget import TabWidget
from .confirmation_dialog import ConfirmationDialog

class MainUI(QWidget):
	"""
	A GUI for standardizing EPICS magnets.

	This GUI utilizes uses :class:`StandardizePanel` to allow users to 
	emit a signal with their selection of magnets. Users must go through
	a confirmation screen to emit the signal. This GUI uses :class:`TabWidget`
	to display magnets from different beamlines seperately, and allows more 
	QSS styling flexibility. 

	Attributes
	----------
	standardize_confirmed : pyqtSignal(dict)
		Emitted if the user confirms their standardize request. The signal carries a 
		dictionary mapping all currently selected magnet names to their status messages.

	"""
	standardize_confirmed = pyqtSignal(dict)

	def __init__(self):
		super().__init__()
		self.setWindowTitle('Python standardize')
		self.tabs = TabWidget()

		main_layout = QVBoxLayout()
		main_layout.addWidget(self.tabs)
		self.setLayout(main_layout)

	def make_new_standarize_tab(self, tab_name, healthy_magnets, nonhealthy_magnets):
		tab = StandardizePanel(healthy_magnets, nonhealthy_magnets)
		tab.standardize_requested.connect(self._handle_standardize_request)
		self.tabs.addTab(tab, tab_name)


	def _handle_standardize_request(self, magnets):
		"""
		Raises a confirmation dialog. If confirmed, emits a signal
		with a dictionary mapping magnet names to status messages
		for all currently selected magnets.

		Parameters
		----------
		magnets : dict[str, str]
			a mapping of magnet names to status messages for all
			currently selected magnets.
		"""
		dialog = ConfirmationDialog(parent=self, warning_text="This will trip BCS for BOTH machines.\nPlease check with the other program.")
		result = dialog.exec_()

		if result == dialog.Accepted:
			self.standardize_confirmed.emit(magnets)

