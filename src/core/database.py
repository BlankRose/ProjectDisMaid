from pathlib import Path
import pandas

class Database():
	"""
	Database class to handles anything related to storing data,
	using Pandas module

	Attributes:
	- `folder`: string (path)

	Methods:
	- `_init_` (self, folder: str = "data") -> None
	"""

	#==-----==#

	folder: str
	file: str

	entries = ['id']
	db: pandas.DataFrame

	#==-----==#

	def __init__(self, file: str, folder: str = "data"):
		if not Path.exists(folder):
			Path.mkdir(folder)
		self.folder = folder
		self.file = file
		if not Path.exists(file):
			self.db = None
		self.db = pandas.read_csv(file)

	#==-----==#
