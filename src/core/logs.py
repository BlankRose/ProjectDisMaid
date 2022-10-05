from pathlib import Path
import logging
import os

class Logs():
	"""
	Logging class for easier handling with the `logging` module

	Attributes:
	- `folder`: string (path)
	- `file`: string (path)

	Methods:
	- `_init_` (self, folder: str = "logs", file: str = "latest.log") -> None
	- `clean` (self, keep: int) -> None
	- `danger` (msg: str) -> None
	"""

	#==-----==#

	folder = ""
	file = ""

	#==-----==#

	def __init__(self, folder: str = "logs", file: str = "latest.log") -> None:
		"""
		Initialize a new log class object, with specified path to the `folder`
		and of the name of the currently used `file`

		- `FOLDER` = folder where is gonna be stored logs files
		- `FILE` = name of the currently used log file
		"""
		if not Path.exists(folder):
			Path.mkdir(folder)
		self.folder = folder
		self.file = folder.joinpath(file)

	#==-----==#

	def clean(self, keep: int) -> None:
		"""
		Clear the folder referenced by `Logs.folder`, of all its logs except the current one
		and the specified amount by `keep`
		
		- `KEEP` = amount of log files to keep
		"""
		logs = []
		for f in os.listdir(self.folder):
			f = self.folder.joinpath(f)
			if os.path.isfile(f) and f.as_posix().endswith(".log"):
				logs.append(f)
		logs.sort(key=lambda t:-os.stat(t).st_mtime)
		if keep == 0:
			keep = 1
		if keep > 0:
			logging.debug("Searching for excess of logs and cleaning..")
			for excess in logs[keep:]:
				os.remove(excess)
			logging.debug("Cleaning done!")

	#==-----==#

	def danger(msg: str):
		"""
		Uses logging to send a critical log, using `msg` as its output then abort the programm
		
		- `MSG` = message to display in the logs
		"""
		logging.critical(msg)
		os.abort()