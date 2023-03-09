# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - construct.py                          #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Thu Mar  9 15:41:33 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

import datetime
import discord

def max_time() -> datetime.datetime:
	return datetime.datetime(9999, 12, 31, 23, 59, 59, 999999)

def parse_time(time: str) -> datetime.datetime:
	time = time.replace(" ", "").replace("	", "")
	if time.lower() == "inf" or time.lower() == "infinite": return max_time()
	result = datetime.datetime.now().astimezone()
	tmp = ""
	for i in time:
		if i.isdigit(): tmp += i
		else:
			if i != 'y' and i != 'd' and i != 'h' and i != 'm' and i != 's': return
			try:
				if tmp == "": continue
				if i == 'y': result += datetime.timedelta(days = int(tmp) * 365)
				if i == 'd': result += datetime.timedelta(days = int(tmp))
				if i == 'h': result += datetime.timedelta(hours = int(tmp))
				if i == 'm': result += datetime.timedelta(minutes = int(tmp))
				if i == 's': result += datetime.timedelta(seconds = int(tmp))
			except OverflowError: return
			tmp = ""
	return result

def parse_hexa(data: str) -> int:
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

async def reply(ctx: discord.Interaction, msg: str = None, ephemeral: bool = True) -> None:
	if not msg: await ctx.response.send_message("Task completed!", ephemeral = ephemeral, delete_after = 10)
	else: await ctx.response.send_message(msg, ephemeral = ephemeral)

def import_entries(imports, dir: str = ""):
	"""
	Imports and returns a list of imported elements.

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

	entries: dict[str, ] = {}
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