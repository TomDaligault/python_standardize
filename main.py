from presenter import Presenter
from epics_magnet_interface import EpicsMagnetInterface
from main_ui import MainUI

from PyQt5.QtWidgets import QApplication
import sys

background_0 = '#202020'
background_1 = '#292929'
button = '#363636'
hxr = '#4a9af8'
sxr = '#F06790'
danger = '#d94a4a'
text = '#808080'
scroll_handle_border = '#505050'

stylesheet = f"""
			QWidget {{background-color: {background_0}; color: {text}; font-family: 'Calibri'; font-size: 18px}}
			QWidget#selection {{background-color: {background_1}}}

			QLabel {{padding-top: 6px; padding-bottom: 6px; padding-left: 2px; padding-right: 2px}}

			QPushButton {{background-color: {button}; border-radius: 6px; padding: 6px 18px; outline: none; }}
			QPushButton:hover, QPushButton:focus {{ border: 1px solid {text}}}

			QPushButton:hover#tab_button_HXR, QPushButton:checked#tab_button_HXR {{background-color: {hxr}; color: {background_0}; border-width: 0px}}
			QPushButton:hover#tab_button_SXR, QPushButton:checked#tab_button_SXR {{background-color: {sxr}; color: {background_0}; border-width: 0px}}


			QPushButton:hover#standardize_button, QPushButton:focus#standardize_button {{ color: {danger}; border: 1px solid {danger}}}

			QCheckBox {{background-color: {background_1};}}
			QCheckBox:focus, QCheckBox:hover {{outline: none; padding-left: 2px;}}

			QScrollArea {{border: none}}

			QScrollBar {{ background: {button}; width: 4px; margin: 0px; }}
			QScrollBar::handle {{ background-color: {background_1}; border: 1px solid {scroll_handle_border}; }}
			QScrollBar::add-line, QScrollBar::sub-line {{ width: 0px; background: none; border: none; }}
			QScrollBar::add-page, QScrollBar::sub-page {{ background: {background_1};}}
			
			"""

if __name__ == '__main__':
	app = QApplication(sys.argv)
	magnet_interface = EpicsMagnetInterface()
	ui = MainUI()
	ui.setStyleSheet(stylesheet)
	presenter = Presenter(magnet_interface, ui)
	ui.show()
	sys.exit(app.exec_())