from presenter.presenter import Presenter

from model.epics_magnet_interface import EpicsMagnetInterface

from view.main_ui import MainUI
import view.stylesheets as styles

from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
	app = QApplication(sys.argv)
	magnet_interface = EpicsMagnetInterface()
	ui = MainUI()
	ui.setStyleSheet(styles.dark_mode)
	presenter = Presenter(magnet_interface, ui)
	ui.show()
	sys.exit(app.exec_())