# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - locals.py                             #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Sun May 14 18:49:25 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

import json
from pathlib import Path
from typing import Any

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

	#==-----==#

def get_local(lang: str, local: str, sep: str = '\n') -> str:

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
		return load
	elif type(load) is list:
		output: str = ""
		for i in load:
			if type(i) is not str:
				return local
			output += i
			if i is not load[-1]:
				output += sep
		return output
	return trigger_fallback()

	#==-----==#

def get_raw_locals() -> dict[str, Any]:
	return localizations
