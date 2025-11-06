from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

from epics_magnet_interface import EpicsMagnetInterface
from standardize_panel import StandardizePanel
from tab_widget import TabWidget
from confirmation_dialog import ConfirmationDialog

class MainUI(QWidget):
	"""
	A GUI for standardizing EPICS magnets.

	"""

	def __init__(self):
		super().__init__()
		self.setWindowTitle('Python standardize')
		self.tabs = TabWidget()

		main_layout = QVBoxLayout()
		main_layout.addWidget(self.tabs)
		self.setLayout(main_layout)

	def setup_standardize_panels(self, hxr_magnets_by_health, sxr_magnets_by_health, on_standardize):
		self.hxr_tab = StandardizePanel(*hxr_magnets_by_health.values(), on_standardize)
		self.sxr_tab = StandardizePanel(*sxr_magnets_by_health.values(), on_standardize)

		self.tabs.addTab(self.hxr_tab, "HXR")
		self.tabs.addTab(self.sxr_tab, "SXR")   


	def raise_confirmation(self, on_confirm):
		dialog = ConfirmationDialog(parent=self, warning_text="This will trip BCS for BOTH machines.\nPlease check with the other program.")
		result = dialog.exec_()

		if result == dialog.Accepted:
			on_confirm()