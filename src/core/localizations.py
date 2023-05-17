# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - locals.py                             #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Wed May 17 13:48:06 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

import json
from src.core import database
from pathlib import Path
from typing import Any

available: list[str] = []
localizations: dict[str, Any] = {}
FALLBACK: str = "en-us"

	#==-----==#

def load_locals(folder: Path | str) -> None:

	if type(folder) is str:
		folder = Path(folder)
	if type(folder) is None or not folder.exists():
		return

	for target in folder.iterdir():
		if target.is_file():
			with open(target) as f:
				localizations[target.name] = json.load(f)
				available.append(target.name)

	#==-----==#

def inplace_strings(content: str, *args: str) -> str:
	for i, arg in enumerate(args):
		placeholder = "{{" + str(i) + "}}"
		content = content.replace(placeholder, arg)
	return content

	#==-----==#

def get_local(lang: str, local: str, *args: str, sep: str = '\n') -> str:

	def trigger_fallback() -> str:
		if type(lang) is None or lang is not FALLBACK:
			return get_local(FALLBACK, local, sep)
		else: return local

	if type(local) is None or type(local) is not str or not len(local):
		return ""
	if type(lang) is None or type(lang) is not str or not lang in localizations.keys():
		return trigger_fallback()

	path = local.split('.')
	load: Any = None

	if not len(path):
		return ""
	try:
		load = localizations[lang][path[0]]
		path.remove(path[0])

		for i in path:
			load = load[i]
	except:
		return trigger_fallback()

	if type(load) is str:
		return inplace_strings(load, *args)
	elif type(load) is list:
		output: str = ""
		for i in load:
			if type(i) is not str:
				return local
			output += i
			if i is not load[-1]:
				output += sep
		return inplace_strings(output, *args)
	return trigger_fallback()

	#==-----==#

def get_raw_locals() -> dict[str, Any]:
	return localizations

	#==-----==#

def get_userlang(user_id: int):
	return database.fetch(-1, user_id, 'lang')
