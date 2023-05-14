# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - random.py                             #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Sun May 14 17:38:21 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.core.locals import get_local
import numpy as np
import logging
import discord

class Random:

	LOC_BASE = "command.scripts.random"
	COMMAND = "random"
	ALIAS = ["roll", "dice", "rng"]
	ICON = "🎲"

	MAX_ROLLS =                100_000_000
	MAX_VALUE =  9_223_372_036_854_775_807
	MIN_VALUE = -9_223_372_036_854_775_808

	#==-----==#

	def parseArgs(self, arg: str) -> tuple[int, int, int]:
		""" Parses argument and returns a tuple (rolls, min, max) """
		rolls: int | str = 1
		min: int | str = 1
		max: int | str = 6
		cur: list[str] = arg.split("d")

		arg = arg.replace("_", "")
		if not str.startswith(arg, "d"):
			rolls = cur[0]

		if len(cur) > 1 and cur[1]:
			if cur[1].find("..") != -1:
				if cur[1].find(",") != -1 or cur[1].find("..", cur[1].find("..") + int(1)) != -1:
					return (-1, 0, 0)
				cur = cur[1].split("..")
				if cur[0]:
					min = cur[0]
					if not cur[1]:
						max = 300
				if cur[1]:
					max = cur[1]
					if not cur[0]:
						min = 0
			else:
				max = cur[1]

		logging.debug(f"ROLLS: {rolls} =-= MIN: {min} =-= MAX: {max}")

		try:
			if int(max) < int(min):
				tmp = max
				max = min
				min = tmp
			ret: tuple[int, int, int] = (int(rolls), int(min), int(max))
		except:
			logging.debug("Invalid Arguments...")
			return (-1, 0, 0)

		if ret[2] > Random.MAX_VALUE or ret[1] < Random.MIN_VALUE:
			logging.debug("Beyong MIN and MAX limits!")
			return (-1, 0, 0)
		return ret

	#==-----==#

	def newRoll(self, args: tuple[int, int, int]) -> np.ndarray:
		""" Roll with given tuple (rolls, min, max) and returns a list of values """
		return np.random.randint(args[1], args[2] + 1, args[0])

	#==-----==#

	def displayRoll(self, values: np.ndarray) -> str:
		""" Converts a list of values into a displayable string """

		display = str("")
		if values.size <= 50:

			if values.size > 1:
				display += "Values: "
			else:
				display += "Value: "

			first = bool(True)
			for i in values:
				if first:
					display += str(i)
					first = False
				else:
					display += ", " + str(i)
				if len(display) > 200:
					display = "Too many values to display!"
					break
		else:
			display = "Too many values to display!"

		if values.size > 1:
			display += "\nTotal:   " + str(np.sum(values))
			display += "\nAverage: " + str(np.average(values))
		return display

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:
		registry = self.ALIAS + [self.COMMAND]
		short = self.ICON + " " + get_local("en-us", f"{self.LOC_BASE}.short")
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = short)
			@discord.app_commands.describe(arguments = f"List of random sets (/help {self.COMMAND} for details)")
			async def run(ctx: discord.Interaction, arguments: str = None):

				await ctx.response.defer(ephemeral = True, thinking = True)

				total_rolls: int = 0
				args: list[str] = []
				if arguments:
					args = arguments.split(" ")
				res: list[tuple[int, int, int]] = [(-1, 0, 0)] * len(args)
				if len(args) > 0:
					for i, v in enumerate(args):
						res[i] = self.parseArgs(v)
						if res[i][0] < 0:
							return await ctx.followup.send(f"I cant understand your request..\nPlease look up the syntax with `/help {self.COMMAND}`!")
						total_rolls += res[i][0]

				if total_rolls > Random.MAX_ROLLS:
					return await ctx.followup.send(f"Sorry but I'd rather limit this to {Random.MAX_ROLLS} rolls!\nWhy the heck you want that many anyway?\nTotal rolls given: {total_rolls}..")

				embed = discord.embeds.Embed()
				embed.color = 0xEB9234
				embed.title = f"**{ctx.user.display_name}'s Roll Results**"
				file = discord.File("assets/dices.png", filename="dices.png")
				embed.set_thumbnail(url="attachment://dices.png")

				if len(args) > 0:
					for i, v in enumerate(res):
						embed.add_field(
							name = args[i],
							value = self.displayRoll(self.newRoll(v)),
							inline = True )
				else:
					embed.description = self.displayRoll(self.newRoll((1, 1, 6)))
				await ctx.followup.send("I've noted down your results below:", file = file, embed = embed)
