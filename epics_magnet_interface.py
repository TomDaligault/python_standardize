# from meme import names
# from epics import caget_many

class EpicsMagnetInterface:
	"""
	A lightweight tool for interfacing with EPICS for magnet standardization.

	Attributes
	----------
	primaries : list[str]
		Magnet types to include when filtering PVs.

	beamline_regions : dict[str, list[str]]
		Maps beamline identifiers to lists of region identifiers.

	healthy_statuses : set[str]
		Status messages considered "healthy" when classifying magnets.

	Notes
	-----
	- Retrieval is dynamic to accommodate magnet installation/removal over time.
	- In this tool, *magnets* specifically refers to a dictionary mapping
	magnet names to their status messages. For consistency, all public methods 
	accept or return this mapping (or collections of such mappings) where applicable. 
	"""

	primaries = ['BEND', 'QUAD']

	beamline_regions = {
					'HXR': ['CLTH', 'BSYH', 'LTUH', 'DMPH'],
					'SXR': ['CLTS', 'BSYS', 'LTUS', 'DMPS'],
					} 

	healthy_statuses = {'Good', 'BCON Warning', 'BDES Change', 'Not Stdz\'d', 'Out-of-Tol', 'BAD Ripple'}

	def get_magnets_by_health(self, beamline):
		"""
		Gets a map of magnet names and statuses grouped by health for
		a given beamline indentifer.

		Parameters
		----------
		beamline : str
			Beamline identifier to retrieve data from.

		Returns
		-------
		dict[str, dict[str, str]]
		    A dictionary with two keys: 'healthy' and 'nonhealthy'.
		    Each maps magnet names to their corresponding status messages.
		"""

		magnets = self.get_magnets(beamline)
		return self._partition_by_health(magnets)


	def get_magnets(self, beamline: str):
		"""
		Builds a map between magnet names and statuses for a given beamline identifier.

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

		Parameters
		----------
		magnet_names : list[str]
			The list of magnet names to filter.
		"""

		device_configs = caget_many([name + ':CONFIG' for name in magnet_names])
		names_and_configs = dict(zip(magnet_names, device_configs))
		return [name for name, config in names_and_configs.items() if config != 'String']

	def _partition_by_health(self, magnets):
		"""
		Split magnets into healthy and nonhealthy group based on status messages.

		Parameters
		----------
		magnets : dict[str, str]
			A map between magnet names and statuses.

		Returns
		-------
		dict[str, dict[str, str]]
			A map between health group, name names, and magnet statuses.

		Notes
		-----
		- Uses the class-level `healthy_statuses` for categorization into groups.
		"""

		healthy_magnets = {m: s for m, s in magnets.items() if s in self.healthy_statuses}
		nonhealthy_magnets = {m: s for m, s in magnets.items() if s not in self.healthy_statuses}

		return {'healthy': healthy_magnets, 'nonhealthy': nonhealthy_magnets}