# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - construct.py                          #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Mon Mar  6 17:15:02 CET 2023      #
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