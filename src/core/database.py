# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - database.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Sun May 21 21:49:56 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

from typing import Any
from .configs import Config
import time, logging as logs

import sqlite3 as sqlLocal
import mysql.connector as sqlServer

	#==-----==#

class Storage:

	conn: sqlLocal.Connection | sqlServer.MySQLConnection = None

	RESERVED: dict[int, tuple[str, dict[str, Any]]] = {
		0: ('default', {
				'id': -1,
				'xp': 0,
				'level': 0,
				'warns': 0,
				'chess': -1,
		}),
		-1: ('shared', {
				'id': -1,
				'lang': 'en-us'
		}),
		-2: ('servers', {
				'id': -1,
				'xp_enabled': False,
				'logs_enabled': False
		})}
	"""
	Contains information about what are the expected structure and
	its default values whenever new entries are created.
	 - USAGE: {id: (name, {entry: default})}
	 - ID 0 represents single server savestate
	"""

	def __init__(self, *_) -> None:
		raise NotImplementedError

	#==-----==#

def connect(user: str, password: str, host: str, port: str, name: str,
		retries: int, timer: int) -> bool:
	"""
	Connect to the MySQL database using the various
	arguments provided and returns False if all tries failed
	"""

	# Definition of a single attempt
	def new_attempt(i: int) -> bool:
		try:
			logs.info(f"Trying to connect to database.. (Attempt {i + 1})")
			if Config.data['local']:
				Storage.conn = sqlLocal.connect(name + '.db')
				return True
			else:
				Storage.conn = sqlServer.connect(
					user = user,
					password = password,
					host = host,
					port = port,
					database = name)
				if Storage.conn.is_connected():
					return True
		except Exception as err:
			logs.error(f"Failed to connect: {err}")
			Storage.conn = None
		return False

	# Destroys older connection
	if Storage.conn: disconnect()

	# Unlimited Retries
	if retries <= 0:
		i = 0
		while new_attempt(i) is False:
			time.sleep(timer)
			i += 1
		return True

	# Limited Retries
	for i in range(retries):
		if i != 0:
			time.sleep(timer)
		if new_attempt(i):
			return True
	logs.error(f"All {retries} attempts to connect to database has failed!")
	return False

	#==-----==#

def disconnect() -> None:
	"""
	Save the current data and
	disconnect the connection if any exists
	"""

	if Storage.conn:
		Storage.conn.commit()
		Storage.conn.close()
		logs.info("Database has been disconnected!")
	Storage.conn = None

	#==-----==#

def create_savestate(id: int) -> None:
	"""
	Creates a fresh new savestate ready to use
	"""

	# Assign table name
	# (stringified id if server, otherwise special name for RESERVEDs)
	if id < 0 and id in Storage.RESERVED.keys():
		table = Storage.RESERVED[id][0]
	else:
		table = f"guild_{id}"
		id = 0

	# Finally create table if doesn't exists
	# and commit changes if successful
	cur = Storage.conn.cursor()
	columns = Storage.RESERVED[id][1].keys()

	try:
		cur.execute(f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(columns)})")
		Storage.conn.commit()
	except Exception as err:
		logs.error(f"Couldn't create a new savestate: {err}")

	#==-----==#

def store(table_id: int, user_id: int, data: dict[str, Any] | Any, name: str = None) -> None:
	"""
	Saves the given data within the storage for the given guild or
	shared savestates for a designed user, and it can be further more
	specific by giving the data name.

	NOTE: Automatly creates a new savestates if it is missing
	"""

	# Retrieve table name
	# (stringified id if server, otherwise special name for RESERVEDs)
	server_id = table_id
	if table_id < 0 and table_id in Storage.RESERVED.keys():
		table = Storage.RESERVED[table_id][0]
	else:
		table = f"guild_{table_id}"
		table_id = 0

	# Retrieve some needed structures
	cur = Storage.conn.cursor()
	columns = Storage.RESERVED[table_id][1].keys()

	# Checks if table exist, otherwise create it
	if isinstance(Storage.conn, sqlLocal.Connection):
		cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
		subst = '?'
	elif isinstance(Storage.conn, sqlServer.MySQLConnection):
		cur.execute(f"SHOW TABLES LIKE '{table}'")
		subst = '%s'
	else:
		logs.error(f"Trying to store but no valid connection is set!")
		return
	if not cur.fetchone():
		create_savestate(server_id)
	if name and name not in columns:
		logs.error(f"Trying to store data to non existant columns!")
		return

	# Retrieve original data
	cur.execute(f"SELECT * FROM {table} WHERE id = {user_id}")
	result = cur.fetchone()
	if not result: result = Storage.RESERVED[table_id][1]
	else: result = dict(zip(columns, result))

	# Update the data with new data
	if not name:
		for k, v in data.items():
			if k in result.keys():
				result[k] = v
	elif name in columns:
		result['id'] = user_id
		result[name] = data

	# Insert into the database results
	try:
		cur.execute(f"SELECT * FROM {table} WHERE id = {user_id}")
		if cur.fetchone():
			update_values = ', '.join(f"{k} = {subst}" for k in result.keys())
			values = tuple(result.values()) + (user_id,)
			cur.execute(f"UPDATE {table} SET {update_values} WHERE id = {subst}", values)
		else:
			placeholders = ', '.join(subst for _ in result.keys())
			values = tuple(result.values())
			cur.execute(f"INSERT INTO {table} ({', '.join(x for x in result.keys())}) VALUES ({placeholders})", values)
		Storage.conn.commit()
	except Exception as err:
		logs.error(f"Error occured while storing data: {err}")

	#==-----==#

def fetch(table_id: int, user_id: int, name: str = None) -> dict[str, Any] | Any | None:
	"""
	Retrieves requested informations for any given guild or
	shared savestates for a designed user, and it can be further more
	specific by giving the data name.

	If it does not exists (yet), it returns default values instead
	(May return None is it is not part of default values either!).

	NOTE: Automatly creates a new savestate if it is missing.
	"""

	# Retrieve table name
	# (stringified id if server, otherwise special name for RESERVEDs)
	server_id = table_id
	if table_id < 0 and table_id in Storage.RESERVED.keys():
		table = Storage.RESERVED[table_id][0]
	else:
		table = f"guild_{table_id}"
		table_id = 0

	# Retrieve some needed structures
	cur = Storage.conn.cursor()
	columns = Storage.RESERVED[table_id][1].keys()
	result = None

	# Checks if table exist, otherwise create it
	if isinstance(Storage.conn, sqlLocal.Connection):
		cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
	elif isinstance(Storage.conn, sqlServer.MySQLConnection):
		cur.execute(f"SHOW TABLES LIKE '{table}'")
	else:
		logs.error(f"Trying to store but no valid connection is set!")
		return
	if not cur.fetchone():
		create_savestate(server_id)

	# No specific entries
	if not name:
		try:
			cur.execute(f"SELECT * FROM {table} WHERE id = {user_id}")
			result = cur.fetchone()
			if result:
				result = dict(zip(columns, result))
				return result
		except Exception as err:
			logs.error(f"Error occured while fetching data: {err}")
		result = Storage.RESERVED[table_id][1]
		result['id'] = user_id
		return result

	# Specific entry
	elif name in columns:
		try:
			cur.execute(f"SELECT * FROM {table} WHERE id = {user_id}")
			result = cur.fetchone()
			if result:
				result = dict(zip(columns, result))
				return result[name]
		except Exception as err:
			logs.error(f"Error occured while fetching data: {err}")
		return Storage.RESERVED[table_id][1][name]

	return None
