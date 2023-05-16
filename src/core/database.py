# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - database.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Tue May 16 17:15:31 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

from typing import Any
from pathlib import Path
import pandas as pd
import logging
import os

class Storage:

	"""
	Storage class with the only purpose to store all of the bot's data

	Attributes
	----------
	folder: `string`
		Relative path to the target folder where is located data files
	server_save: `list[Any]`
		List of all of the available columns, and used as a comparation
		when needing to update the internal dataframe
	shared_save: `list[Any]`
		List of all available columns for the shared savestates, and used
		as a comparation when needing to update the internal dataframe
	data: `dict[int, DataFrame]`
		Dictionary of dataframes containing the saved datas where
		key is guilds' id (entry -1 is reserved for shared savestates)
	"""

	#==-----==#

	folder: str = "data"

	server_save = ['id']
	shared_save = ['id', 'lang']

	SHARED_DEFAULT = pd.Series(data = {
		'lang': 'en-us'
	})
	SERVER_DEFAULT = pd.Series(data = {})

	data: dict[int, pd.DataFrame] = {}
	reserved: dict[int, str] = {-1: 'shared'}

	#==-----==#

def create_savestate(id: int) -> None:
	"""
	Creates a fresh new savestate ready to use
	(If ID is -1, it regens a new shared savestate instead
	of a server savestate)
	"""

	new_db: pd.DataFrame
	if id == -1:
		new_db = pd.DataFrame(columns = Storage.shared_save)
	else:
		new_db = pd.DataFrame(columns = Storage.server_save)
	new_db.set_index('id', inplace = True)
	Storage.data[id] = new_db

	#==-----==#

def save(folder: str = Storage.folder) -> None:
	"""
	Saves the current data to the target file and folder
	"""

	if len(Storage.data):

		fold = Path(folder)
		if not fold.exists():
			fold.mkdir()

		for i, v in Storage.data.items():
			if i in Storage.reserved.keys():
				path = os.path.join(folder, Storage.reserved[i])
			else:
				path = os.path.join(folder, str(i))
			v.to_csv(path)

	else:
		logging.error("SAVE failed! Cannot save data base since none exists!")

	#==-----==#

def load(folder: str = Storage.folder) -> None:
	"""
	Loads the data from a target file and folder
	"""

	fold = Path(folder)
	if not fold.exists():
		fold.mkdir()
	Storage.folder = folder

	for i in fold.iterdir():
		if not i.is_file():
			continue

		key = None
		for k, v in Storage.reserved.items():
			if i.name == v: key = k

		try:
			if key is None:
				key = int(i.name)
			Storage.data[key] = pd.read_csv(i, index_col = 'id')
		except:
			logging.error(f"LOAD failed for file: {i}! Corrupt file?")

	if Storage.data.get(-1, None) is None:
		create_savestate(-1)

	#==-----==#

def store(guild_id: int, user_id: int, data: pd.Series | Any, name: str = None) -> None:
	"""
	Saves the given data within the storage for the given guild or
	shared savestates for a designed user, and it can be further more
	specific by giving the data name.

	NOTE: Automatly creates a new savestates if it is missing
	"""

	db = Storage.data.get(guild_id, None)
	if db is None:
		create_savestate(guild_id)
		db = Storage.data[guild_id]

	if name is None or type(data) == pd.Series:
		db.loc[user_id] = data

	else:
		try:
			if user_id not in db.index:
				if guild_id == -1: db.loc[user_id] = Storage.SHARED_DEFAULT
				else: db.loc[user_id] = Storage.SERVER_DEFAULT
			db.loc[user_id, name] = data
		except:
			return

	#==-----==#

def fetch(guild_id: int, user_id: int, name: str = None) -> pd.Series | Any:
	"""
	Retrieves requested informations for any given guild or
	shared savestates for a designed user, and it can be further more
	specific by giving the data name.

	If it does not exists (yet), it returns default values instead
	(May return None is it is not part of default values either!).

	NOTE: Automatly creates a new savestate if it is missing.
	"""

	db = Storage.data.get(guild_id, None)
	if db is None:
		create_savestate(guild_id)
		db = Storage.data[guild_id]

	if name is None:
		try: return db.loc[user_id]
		except:
			if guild_id == -1: return Storage.SHARED_DEFAULT
			else: return Storage.SERVER_DEFAULT

	else:
		try: return db.loc[user_id, name]
		except:
			try:
				if guild_id == -1: return Storage.SHARED_DEFAULT[name]
				else: return Storage.SERVER_DEFAULT[name]
			except:
				return None
