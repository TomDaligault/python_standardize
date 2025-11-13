from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QStackedWidget

class TabWidget(QWidget):
	"""
	A custom tab widget with increased styling flexibility.

	This widget uses toggleable buttons to switch between pages
	displayed in an internal :class:`QStackedWidget`. It provides
	a lightweight alternative to :class:`QTabWidget` with greater
	control over appearance and layout.
	
	Tab buttons can be targeted in QSS via the object name `tab_button_<name>`.

	"""
	def __init__(self):
		super().__init__()

		self.tab_button_layout = QHBoxLayout()
		self.tab_button_layout.setSpacing(0)

		self.tab_pages = QStackedWidget()

		main_layout = QVBoxLayout(self)
		main_layout.addLayout(self.tab_button_layout)
		main_layout.addWidget(self.tab_pages)
		main_layout.setSpacing(0)

		self.tab_buttons = []

	def addTab(self, widget: QWidget, name: str):
		"""
		Add a new tab to the widget.

		The first tab added is selected by default.

		Parameters
		----------
		widget : QWidget
			The widget to display when the new tab is selected.
		name : str
			The label for the new tab button. Also used to generate
			the button's QSS object name `tab_button_<name>`.

		"""
		index = self.tab_pages.addWidget(widget)
		button = QPushButton(name)
		button.setCheckable(True)
		button.setAutoExclusive(True)
		button.setObjectName(f"tab_button_{name}")

		button.clicked.connect(lambda checked, i=index: self.tab_pages.setCurrentIndex(i))
		self.tab_button_layout.addWidget(button)
		self.tab_buttons.append(button)

		if len(self.tab_buttons) == 1:
			button.setChecked(True)
			self.tab_pages.setCurrentIndex(0)