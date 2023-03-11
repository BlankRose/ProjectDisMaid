# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - database.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Sat Mar 11 23:44:16 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

from pathlib import Path
import logging
import pandas as pd

class Storage:

	"""
	Storage class with the only purpose to store all of the bot's data

	Attributes
	----------
	folder: `string`
		Relative path to the target folder where is located data files
	file: `string`
		Name of the file to load in and save in
	columns: `list[Any]`
		List of all of the available columns, and used as a comparation
		when needing to update the internal dataframe
	data: `DataFrame`
		Main dataframe containing the saved data
	"""

	#==-----==#

	folder: str = "data"
	file: str = "data.csv"

	columns = ['id']
	data: pd.DataFrame = None

	#==-----==#

def create_default() -> None:
	"""
	Creates a default, ready-to-use, internal dataframe
	"""
	Storage.data = pd.DataFrame(columns = Storage.columns)

	#==-----==#

def save(file: str = Storage.file, folder: str = Storage.folder) -> None:
	"""
	Saves the current data to the target file and folder
	"""

	if Storage.data:
		Storage.data.to_csv(Storage.file)
	else:
		logging.error("SAVE failed! Cannot save data base since none exists!")

	#==-----==#

def load(file: str | None = Storage.file, folder: str = Storage.folder) -> None:
	"""
	Loads the data from a target file and folder
	"""

	if not Path.exists(folder):
		Path.mkdir(folder)
	Storage.folder = folder
	Storage.file = file
	if not file or not Path.is_file(file):
		return create_default()

	Storage.data = pd.read_csv(file)