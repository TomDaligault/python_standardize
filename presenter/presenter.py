class Presenter:
    def __init__(self, magnet_interface, ui):
        self.magnet_interface = magnet_interface
        self.ui = ui

        hxr_magnets_by_health = self.magnet_interface.get_magnets_by_health('HXR')
        sxr_magnets_by_health = self.magnet_interface.get_magnets_by_health('SXR')
      
        self.ui.make_new_standarize_tab("HXR", *hxr_magnets_by_health.values())
        self.ui.make_new_standarize_tab("SXR", *sxr_magnets_by_health.values())
        self.ui.standardize_confirmed.connect(self.start_standardize)

    def start_standardize(self, magnets):
    		self.shutter_beams()
            self.magnet_interface.standardize(magnets)
            self.launch_striptool(magnets)
            self.ui.close()

    def shutter_beams(self):
    	"""
    	Not implemented. Always shutter both NC and SC feels like the safest move here.
    	"""
    	pass

    def launch_striptool(self):
    	"""
		Not implemented. Need to see if Michael's striptool + archiver can be launched programatically.
    	"""
        pass


