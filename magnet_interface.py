from meme import names
from epics import caget

class MagnetInterface:
	"""
	A lightweight tool for interfacing with EPICS magnets for beamline standardization.

	Provides methods to retrieve magnet control PVs, filter magnets by status, and initiate 
	 standardization. Designed for dynamic runtime discovery of magnets.

	Attributes
	----------
	primaries : set[str]
		Magnet types to include when filtering PVs.

	beamline_regions : dict[str, set[str]]
		Maps beamline names to sets of region identifiers.

	healthy_statuses : set[str]
		Status messages considered "healthy" when filtering magnets.

	Notes
	-----
	- Retrieval is dynamic to account for magnet installation/removal over time. 
	- Only PV names are stored; actual PV access is done via `caget` and `caput` as necessary.

	"""
	primaries = {'BEND', 'QUAD'}

	beamline_regions = {
					'HXR': {'CLTH', 'BSYH', 'LTUH', 'DMPH'},
					'SXR': {'CLTS', 'BSYS', 'LTUS', 'DMPS'},
					} 

	healthy_statuses = {'Good', 'BCON Warning', 'BDES Change', 'Not Stdz\'d', 'Out-of-Tol', 'BAD Ripple'}

	def __init__(self, primaries=None, beamline_regions=None, healthy_statuses=None):
		"""
		Initialize indentifiers used for magnet parameter retreival and filtering.

		Defaults to class-level values unless overridden by user-specified values.

		Parameters
		----------
		primaries : set[str]
			Magnet types to include when filtering PVs.

		beamline_regions : dict[str, set[str]]
			Maps beamline names to sets of region identifiers.

		healthy_statuses : set[str]
			Status messages considered "healthy" when filtering magnets.
		"""
		
		self.primaries = primaries or self.__class__.primaries
		self.beamline_regions = beamline_regions or self.__class__.beamline_regions
		self.healthy_statuses = healthy_statuses or self.__class__.healthy_statuses

	def get_magnets(self, beamline: str) -> dict[str, str]:
		"""
		Retrieve magnet BCTRL PV names and corresponding status messages for a beamline. 

		Parameters
		----------
		beamline : str
			Beamline name to retieve magnets from.

		Returns
		-------
		dict[str, str]
			Mapping magnet BCTRL PV names to status messages (from STATMSG PV).

		Notes
		-----
		- Only magnets with valid STATMSG PVs are included.
		- STATMSG PVs are converted to BCTRL PV names for consistence.
		"""
		regions = self.beamline_regions[beamline]
		status_pv_names = self._get_status_pv_names(regions)
		return {status_pv.replace("STATMSG", "BCTRL"): caget(status_pv, as_string=True) for status_pv in status_pv_names}


	def filter_magnets(self, magnets: dict[str, str], healthy_statuses=None):
		"""
		Split a dictionary of magnets into healthy and unhealthy based on status messages.

		Parameters
		----------
		magnets : dict[str, str]
			Dictionary of magnet BCTRL PV names mapped to their current status messages.
		healthy_statuses : set[str], optional
			Set of status strings considered "healthy". 
			If None, uses the class attribute `healthy_statuses`.

		Returns
		-------
		healthy_magnets : dict[str, str]
			Magnets whose statuses are in `healthy_statuses`.
		unhealthy_magnets : dict[str, str]
			Magnets whose statuses are not in `healthy_statuses`.

		Notes
		-----
		- Intended for use on dictionaries returned by `get_magnets`.
		"""

		if healthy_statuses is None:
			healthy_statuses = self.healthy_statuses

		healthy_magnets = {k: v for k, v in magnets.items() if v in self.healthy_statuses}
		unhealthy_magnets = {k: v for k, v in magnets.items() if v not in self.healthy_statuses}
		return healthy_magnets, unhealthy_magnets

	def standardize_magnets(self, magnets):  
		"""
		Not yet implimented, I don't want to take down the machines. 
		"""

		print("The following magnets would have been standardized:" + '\n    '.join(magnets))

	def _get_status_pv_names(self, regions: set[str]) -> set[str]:

		"""
		Retrieve STATMSG PV names for a given set of regions.

		Parameters
		----------
		regions : set[str]
			Region identifiers used to filter PV names.
			Typically obtained from `self.beamline_regions[beamline]`.

		Returns
		-------
		set[str]
			Set of matching STATMSG PV names.

		Raises
		------
		NameError
			If no STATMSG PVs are found for the given regions.

		Notes
		-----
		- Constructs a MEME filter string from class-level `primaries` and the provided regions.
		- Could be generalized to retrieve arbitrary PV suffixes instead of just STATMSG.
		"""

		name_filter = f"({'|'.join(self.primaries)}):({'|'.join(regions)})|%|STATMSG"
		status_pv_names = {pv for pv in names.list_pvs(name_filter)}

		if not status_pv_names:
			raise NameError(f"No status PVs found for primaries:{' '.join(self.primaries)}, and regions:{' '.join(regions)}.")

		return status_pv_names
			