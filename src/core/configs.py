import logging
import json

class Config():
	"""
	Config class to handle configurations files (stored in `.json` files)

	Attributes:
	- `data`: dict

	Methods:	
	- `fecth` (self, folder: str, file: str) -> None
	- `save` (data: dict, folder: str, file: str) -> None
	- `check` (data: dict, important: tuple, options: tuple) -> bool
	"""

	#==-----==#
	
	data = {}

	#==-----==#

	def fetch(self, folder: str, file: str) -> None:
		"""
		Gather configs from the `file`, located inside `folder`'s path and
		saves it locally inside the Class (`Config.data`)

		- `FOLDER` = full path to the file's folder
		- `FILE` = name of the file
		"""
		logging.info(f"Fetching data from {file}..")
		with open(folder.joinpath(file), "r") as f:
			try:
				self.data = json.load(f)
			except:
				logging.warning("Couldn't fetch any data!")
				return
		logging.info("Successfully gathered data!")
	
	#==-----==#

	def save(data: dict, folder: str, file: str) -> None:
		"""
		Save the `data` within the provided `file`, located inside the `folder`, for later use!

		- `DATA` = data to save
		- `FOLDER` = full path to the file's folder
		- `FILE` = name of the file
		"""
		logging.info(f"Saving data to {file}..")
		with open(folder.joinpath(file), "w") as f:
			try:
				json.dump(data, f, indent=4)
			except:
				logging.warning("Couldn't save data!")
				return
		logging.info("Successfully saved data!")
	
	#==-----==#

	def check(self, verify: dict, important: tuple, options: tuple) -> bool:
		"""
		Check for the validity of the provided `data` using the tuples `important` and `options`.

		- `VERIFY` = data dictionary to check
		- `IMPORTANT` = tuples of entry, type pairs to be checked and raises and error if check failed
		- `OPTIONS` = tuples of entry, type, default trios to be check and changes the entry to default if check failed

		RETURNS: True if validation passed OR False if validation failed for `Important` entries
		"""
		for i in important:
			try:
				if not isinstance(verify[i[0]], i[1]):
					raise TypeError
			except TypeError:
				logging.warning(f"Expected an {i[1]} for IMPORTANT config: {i[0]}!")
				return False
			except:
				logging.warning(f"Missing IMPORTANT config: {i[0]}! ABORTING!")
				return False

		for i in options:
			try:
				if not isinstance(verify[i[0]], i[1]):
					raise TypeError
			except TypeError:
				logging.warning(f"Expected an {i[1]} for option config {i[0]}. Initializing to default: {i[2]}")
				verify[i[0]] = i[2]
			except:
				logging.warning(f"Missing option config: {i[0]}. Initializing to default: {i[2]}")
				verify[i[0]] = i[2]

		logging.debug(f"Successfully checked data: {verify}")
		return True