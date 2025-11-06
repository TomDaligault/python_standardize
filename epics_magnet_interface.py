# from meme import names
# from epics import caget_many

class EpicsMagnetInterface:
	"""
	A lightweight tool for interfacing with EPICS magnets for beamline standardization.

	Attributes
	----------
	primaries : list[str]
		Magnet types to include when filtering PVs.

	beamline_regions : dict[str, list[str]]
		Maps beamline names to lists of region identifiers.

	healthy_statuses : set[str]
		Status messages considered "healthy" when filtering magnets.

	Notes
	-----
	- Retrieval is dynamically to account for magnet installation/removal over time.

	"""
	primaries = ['BEND', 'QUAD']

	beamline_regions = {
					'HXR': ['CLTH', 'BSYH', 'LTUH', 'DMPH'],
					'SXR': ['CLTS', 'BSYS', 'LTUS', 'DMPS'],
					} 

	healthy_statuses = {'Good', 'BCON Warning', 'BDES Change', 'Not Stdz\'d', 'Out-of-Tol', 'BAD Ripple'}

	def get_magnets_by_health(self, beamline):
		magnets = self.get_magnets(beamline)
		return self._partition_by_health(magnets)


	def get_magnets(self, beamline: str):
		"""
		Builds a map between magnet names and statuses for a given beamline indentifier.

		Parameters
		----------
		beamline : str
			Beamline identifier to retieve magnet names from.

		Returns
		-------
		dict[str, str]
			A map of magnet names as 'PRIMARY:REGION:UNIT' to their status message.

		Notes
		-----
		- Constructs a MEME filter string from class-level `primaries` and `beamline_regions[beamline]`.
		- Excludes all slave magnets as determined by their `:CONFIG` PV.
		"""

		name_filter = f"({'|'.join(self.primaries)}):({'|'.join(self.beamline_regions[beamline])})"

		magnet_names = names.list_devices(name_filter)
		magnet_names = self._remove_string_magnets(magnet_names)

		statuses = caget_many([name + ':STATMSG' for name in magnet_names])

		return dict(zip(magnet_names, statuses))

	def standardize(self, magnets):  
		"""
		Not yet implemented, I don't want to take down the machines. 
		"""

		print('The following magnets would have been standardized:\n    ' + '\n    '.join(magnets))

	def _remove_string_magnets(self, magnet_names):
		"""
		filters out units without dedicated power supplies from a list of magnet names. 
		"""

		device_configs = caget_many([name + ':CONFIG' for name in magnet_names])
		names_and_configs = dict(zip(magnet_names, device_configs))
		return [name for name, config in names_and_configs.items() if config != 'String']

	def _partition_by_health(self, magnets):
		"""
		Split magnets into healthy and nonhealthy group based on status messages.

		Parameters
		----------
		magnets : list[Magnet]

		Returns
		-------
		dict[str: dict[Magnet: str]]
			A map between health group, Magnet objects, and magnet statuses.

		Notes
		-----
		- Uses the class-level `healthy_statuses` for categorization into groups.
		"""

		healthy_magnets = {m: s for m, s in magnets.items() if s in self.healthy_statuses}
		nonhealthy_magnets = {m: s for m, s in magnets.items() if s not in self.healthy_statuses}

		return {'healthy': healthy_magnets, 'nonhealthy': nonhealthy_magnets}