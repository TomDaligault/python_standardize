import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QCheckBox
from PyQt5.QtCore import Qt
from confirmation_dialog import ConfirmationDialog

from epics_magnet_interface import EpicsMagnetInterface
from magnet_selection_widget import MagnetSelectionWidget

class MainUI(QWidget):
	"""
	A GUI for standardizing EPICS magnets.
	"""

	def __init__(self):
		super().__init__()
		self.magnet_interface = EpicsMagnetInterface()
		self._build_ui()

	def on_standardize(self, beamline):
		"""
		Orchestrates the magnet standardization process for the specified beamline.

		Retrieves magnets, filters them into healthy and unhealthy sets, queries the 
		user for confirmation where needed, and performs standardization.

		Parameters
		----------
		beamline : str
			The beamline identifier ("HXR" or "SXR") whose magnets should be standardized.
		"""
		
		dialog = ConfirmationDialog(warning_text="This will trip BCS for BOTH machines.\nPlease check with the other program.")
		result = dialog.exec_()

		if result == dialog.Accepted:
			# magnets = self.magnet_interface.get_magnets(beamline)
			# healthy_magnets, unhealthy_magnets = self.magnet_interface.filter_magnets(magnets)
			healthy_magnets, unhealthy_magnets = {"M1": "Good"}, {"QUAD:LTUH:240": "Offline","QUAD:LTUH:110": "Tripped","QUAD:LTUH:320": "Offline","QUAD:LTUH:540": "Offline","QUAD:LTUH:545": "No Control","QUAD:LTUH:740": "Tripped"}
			permissible_magnets = self.handle_unhealthy_magnets(unhealthy_magnets)

			if permissible_magnets is not None:
				standardize_queue = {**healthy_magnets, **permissible_magnets}
				self.magnet_interface.standardize_magnets(standardize_queue)

				self.launch_striptool(beamline)
				self.close()

	def handle_unhealthy_magnets(self, unhealthy_magnets):
		"""
		Queries the user for permission to standardize non-healthy magnets.

		A confirmation dialog is shown for each magnet with a non-healthy status.
		Approved magnets are tagged with "(overridden)" and returned for inclusion 
		in the standardization queue.

		Parameters
		----------
		unhealthy_magnets : dict[str, str]
			Magnet BCTRL PV names mapped to their current status messages.

		Returns
		-------
		dict[str, str]
			Magnets approved by the user for standardization.
		"""
		selection_widget = MagnetSelectionWidget(unhealthy_magnets)
		dialog = ConfirmationDialog(f"Should we include the following magnets?", selection_widget)
		dialog.resize(340,400)
		result = dialog.exec_()
		if result == dialog.Accepted:
			return selection_widget.get_selected()

	def _on_state_changed(self, magnet, status):
		if checkbox.isChecked():
			self.standardize_queue[magnet] = f"{status} (overridden)"
		else:
			self.standardize_queue[magnet].pop()

	def launch_striptool(self, beamline):
		print("I don't know how to launch Michael's new striptool from python.")


	def _build_ui(self):
		"""
		Constructs the static layout for the main UI.
		"""
		
		hxr_stdz_button = QPushButton(parent=self, text='Standardize HXR')
		sxr_stdz_button = QPushButton(parent=self, text='Standardize SXR')

		hxr_stdz_button.setStyleSheet('background-color: lightblue')
		sxr_stdz_button.setStyleSheet('background-color: pink')

		hxr_stdz_button.clicked.connect(lambda: self.on_standardize(beamline="HXR"))
		sxr_stdz_button.clicked.connect(lambda: self.on_standardize(beamline="SXR"))

		layout = QVBoxLayout()
		layout.addWidget(hxr_stdz_button)
		layout.addWidget(sxr_stdz_button)

		self.setLayout(layout)
		self.setWindowTitle('Python standardize')
		self.resize(340, 100)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainUI()
	window.show()
	sys.exit(app.exec_())