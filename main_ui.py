import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from confirmation_dialog import ConfirmDialog

from magnet_interface_mixin import MagnetInterfaceMixin

class MainUI(MagnetInterfaceMixin, QWidget):
	"""
	A simple PyQt5 GUI for standardizing EPICS magnets.

	Inherits from MagnetInterfaceMixin to interact with EPICS magnets.
	"""

	def __init__(self):
		super().__init__()
		self._build_ui()

	def run_standardize(self, beamline):
		"""
		Orchestrates the magnet standardization process for the specified beamline.

		This method retrieves magnets, filters them into healthy and unhealthy sets,
		queries the user for confirmation where needed, and performs standardization.

		Parameters
		----------
		beamline : str
			The beamline identifier ("HXR" or "SXR") whose magnets should be standardized.
		"""

		magnets = self.get_magnets(beamline)
		healthy_magnets, unhealthy_magnets = self.filter_magnets(magnets)
		permissible_magnets = self.handle_unhealthy_magnets(unhealthy_magnets)
		standardize_queue = {**healthy_magnets, **permissible_magnets}

		dialog = ConfirmDialog(warning_text="This will trip BCS for BOTH machines.\nPlease check with the other program first.")
		result = dialog.exec_()
		if result == dialog.Accepted:
			self.standardize_magnets(standardize_queue)
			self.launch_striptool()

	def handle_unhealthy_magnets(self, unhealthy_magnets):
		"""
		Queries the user for permission to standardize unhealthy magnets.

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
			Magnets approved by the user for forced standardization.

		Notes
		-----
		Repeated pop-ups is a bad user experience.
		"""
		permissible_magnets = {}
 
		for magnet, status in unhealthy_magnets.items():
			dialog = ConfirmDialog(warning_text=f"{magnet} is currently '{status}' should we standardize it anways?")
			result = dialog.exec_()
			if result == dialog.Accepted:
				permissible_magnets[magnet] = f"{status} (overridden)"

		return permissible_magnets

	def launch_striptool(self, beamline):
		pass  # Not sure how to do this. Will ask M. Lans.


	def _build_ui(self):
		"""
		Constructs the static layout for the main UI.
		"""
		
		warning_label = QLabel('<span style="color: red;">Caution, This will Standardize Magnets!</span>', alignment=Qt.AlignCenter)
		hxr_stdz_button = QPushButton(parent=self, text='Standardize HXR')
		sxr_stdz_button = QPushButton(parent=self, text='Standardize SXR')

		hxr_stdz_button.setStyleSheet('background-color: lightblue')
		sxr_stdz_button.setStyleSheet('background-color: pink')

		hxr_stdz_button.clicked.connect(lambda: self.run_standardize(beamline="HXR"))
		sxr_stdz_button.clicked.connect(lambda: self.run_standardize(beamline="SXR"))

		layout = QVBoxLayout()
		layout.addWidget(warning_label)
		layout.addWidget(hxr_stdz_button)
		layout.addWidget(sxr_stdz_button)

		self.setLayout(layout)
		self.setWindowTitle('Python standardize')
		self.resize(300, 100)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainUI()
	window.show()
	sys.exit(app.exec_())