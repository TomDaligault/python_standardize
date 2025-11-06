class Presenter:
	def __init__(self, magnet_interface, ui):
		self.magnet_interface = magnet_interface
		self.ui = ui

		# hxr_magnets = self.magnet_interface.get_magnets_by_health('HXR')
		# sxr_magnets = self.magnet_interface.get_magnets_by_health('SXR')
		
		hxr_magnets_by_health = {'healthy': 
											{'BEND:BSYH:140': 'Not Stdz\'d',
											 'BEND:LTUH:210': 'Not Stdz\'d',
											 'QUAD:LTUH:480': 'Out-of-Tol', 
											 'QUAD:DMPH:740': 'good', 
											 'QUAD:DMPH:741': 'BCON Warning'},
								 'nonhealthy': 
								 			{'BEND:LTUH:240': 'Offline',
											 'QUAD:DMPH:720': 'Offline'}}
		sxr_magnets_by_health ={'healthy': 
											{}, 
								'nonhealthy': 
											{'Q1': 'REALLY bad'}}

		self.ui.setup_standardize_panels(hxr_magnets_by_health, sxr_magnets_by_health, self.on_standardize)

	def on_standardize(self, magnets):
		self.ui.raise_confirmation(lambda m=magnets: self.start_standardize(m))

	def start_standardize(self, magnets):
			self.magnet_interface.standardize(magnets)
			self.launch_striptool(magnets)
			self.ui.close()

	def launch_striptool(self, beamline):
		print("I don't know how to launch Michael's new striptool from python.")


