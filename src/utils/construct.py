# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - construct.py                          #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Wed May 17 14:13:46 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

from typing import Any
import src.core.localizations as lz
import datetime
import discord

def max_time() -> datetime.datetime:
	"""
	Returns the max datatime supported by Python (Year 10000 - 1 us)
	"""
	return datetime.datetime(9999, 12, 31, 23, 59, 59, 999999)

	#==-----==#

def parse_time(time: str) -> datetime.datetime | None:
	"""
	Parse given time into a datetime and returns it.
	Upon error, it returns NONE

	_y_w_d_h_m_s_u:
	 - A series of int-time pair which can contains:
	 - y = years
	 - w = weeks
	 - d = days
	 - h = hours
	 - m = minutes
	 - s = seconds
	 - u = microseconds

	int:
	 - Creates from timestamp

	"inf"/"infinite":
	 - Returns the max_time() value
	"""
	time = time.replace(" ", "").replace("	", "")
	if time.lower() == "inf" or time.lower() == "infinite": return max_time()
	result = datetime.datetime.now().astimezone()
	tmp = ""
	if time.isdecimal():
		result = datetime.datetime.fromtimestamp(float(time))
	else:
		for i in time:
			if i.isdigit(): tmp += i
			else:
				try:
					if tmp == "": continue
					match i:
						case 'y': result += datetime.timedelta(days = int(tmp) * 365.24)
						case 'w': result += datetime.timedelta(weeks = int(tmp))
						case 'd': result += datetime.timedelta(days = int(tmp))
						case 'h': result += datetime.timedelta(hours = int(tmp))
						case 'm': result += datetime.timedelta(minutes = int(tmp))
						case 's': result += datetime.timedelta(seconds = int(tmp))
						case 'u': result += datetime.timedelta(microseconds = int(tmp))
						case _: return
				except OverflowError: return
				tmp = ""
	return result

	#==-----==#

def parse_hexa(data: str) -> int | None:
	value = 0
	for i in data:
		value *= 16
		if (i >= '0' and i <= '9'):
			value += ord(i) - ord('0')
		elif (i >= 'A' and i <= 'F'):
			value += ord(i) - ord('A') + 10
		elif (i >= 'a' and i <= 'f'):
			value += ord(i) - ord('a') + 10
		else:
			return
	return value

	#==-----==#

async def reply(ctx: discord.Interaction, msg: str = None, ephemeral: bool = True) -> None:
	if not msg: await ctx.response.send_message("Task completed!", ephemeral = ephemeral, delete_after = 10)
	else: await ctx.response.send_message(msg, ephemeral = ephemeral)

	#==-----==#

def import_entries(imports: dict[str, str | list[str]] | list[str], dir: str = "") -> dict[str, Any]:
	"""
	Imports and returns a dictionary of imported elements.

	When using a list, it will try to find the name of the element to import with
	the same, in title, as of the module

	When using a dict instead of a list, the key will be the name of the module
	and the value will be the name of the element to import (a list can be given
	to import multiple elements at once from a singular module)
	"""
	import importlib, sys

	if type(dir) is not str: dir = ""
	if len(dir) > 0 and not dir.endswith("."):
		dir += "."

	entries: dict[str, Any] = {}
	if type(imports) is list:
		for i in imports:
			name = dir + i
			try:
				importlib.import_module(name)
				entries[i] = getattr(sys.modules[name], i.title())
			except Exception as err:
				print(err)

	elif type(imports) is dict:
		for k, v in imports.items():
			name = dir + k
			try:
				importlib.import_module(name)
				if v is list:
					entries[k] = [getattr(sys.modules[name], x) for x in v]
				else:
					entries[k] = getattr(sys.modules[name], v)
			except Exception as err:
				print(err)

	else:
		print(f"import_entries() only accepts list or dictionaries as arguments! Provided: {imports.__class__.__name__}")
	return entries

	#==-----==#

def full_description(lang: str, loc_base: str) -> str:

	output: str = ""
	cmd_base: str = "command.base"
	order: list[str] = ["description", "arguments", "sub_arguments", "unspecified", "notes", "permissions"]

	for i in order:
		local = f"{loc_base}.{i}"
		tmp = lz.get_local(lang, local)

		if not tmp == local:
			if not i == order[0]:
				output += "\n\n" + lz.get_local(lang, f"{cmd_base}.{i}") + '\n'
			output += tmp
	return output
