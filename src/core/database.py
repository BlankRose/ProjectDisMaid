# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - database.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Fri Mar 10 15:14:13 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

from pathlib import Path
import logging
import pandas as pd

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

	folder: str = None
	file: str = None

	entries = ['id']
	db: pd.DataFrame = None
	data: ... = None

	#==-----==#

	@staticmethod
	def new_data() -> None:
		pass

	#==-----==#

	@staticmethod
	def save(data: ... = None) -> None:
		if Database.db:
			Database.db.to_csv(Database.file)
		else:
			logging.error("SAVE failed! Cannot save data base since none exists!")

	#==-----==#

	@staticmethod
	def load(file: str, folder: str = "data") -> None:
		if not Path.exists(folder):
			Path.mkdir(folder)
		Database.folder = folder
		Database.file = file
		if not Path.exists(file):
			Database.db = None
		Database.db = pd.read_csv(file)