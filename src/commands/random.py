import logging
import discord
import random as rng
import math

class Random():

	command = "random"
	alias = ["roll", "dice", "rng"]

	syntax = command + " [arguments] ..."
	icon = "🎲"

	short = icon + " Rolls a completely random sets of numbers"
	description = \
"""
A somewhat balanced number randomizer which can receive multiple and \
complex parameters for customized rollings. Look below for details:

__ARGUMENTS:__
`None` - *Generates one random number between 1 and 6*
`X` - *Generates `X` random numbers between 1 and 6*
`XdY` - *Generates `X` random numbers between 1 and `Y`*
`XdY..Z` - *Generates `X` random numbers between `Y` and `Z`*
`XdPATTERN` - *Generates `X` random numbers following given `PATTERN`*

__UNSPECIFIED VALUES:__
`X` - *Will becomes 1*
`Y` - *Will becomes 6 in XdY case or 0 in XdY..Z case*
`Z` - *Will becomes 0*

__SIDE NOTES:__
There can be multiple arguments, each seperated with spaces
`PATTERN` uses values seperated with commas, like here: `3,8,9,6,2`
`X` cannot be a negative value

__REQUIERED PERMISSIONS:__
Application: `None`
Caller: `None`
"""

	#==-----==#

	def parseArgs(self, arg: str) -> tuple:
		""" Parses argument and returns a tuple (rolls, min, max) """
		rolls = 1
		min = 1
		max = 6
		cur = arg.split("d")
		if not str.startswith(arg, "d"):
			rolls = cur[0]
		if cur[1]:
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
		try: # Quick testing output
			int(rolls)
			int(min)
			int(max)
		except: # Invalid arguments are mostly due to invalid given arguments
			return (-1, 0, 0)
		if int(max) < int(min):
			tmp = max
			max = min
			min = tmp
		return (rolls, min, max)

	#==-----==#

	def newRoll(self, args: tuple) -> list:
		""" Roll with given tuple (rolls, min, max) and returns a list of values """
		results = list()
		for i in range(0, int(args[0])):
			results.append(rng.randint(int(args[1]), int(args[2])))
		return results

	#==-----==#

	def displayRoll(self, values: list) -> str:
		""" Converts a list of values into a displayable string """
		display = str("")
		if len(values) > 1:
			display += "Values: "
		else:
			display += "Value: "
		first = bool(True)
		total = int(0)
		for i in values:
			if first:
				display += str(i)
				first = False
			else:
				display += ", " + str(i)
			total += i
		if len(display) > 200:
			display = "Too many values to display!"
		if len(values) > 1:
			display += "\nTotal: " + str(total)
			display += "\nAverage: " + str(math.floor((total / len(values)) * 100) / 100)
		return display

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:
		registry = self.alias + [self.command]
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = self.short)
			@discord.app_commands.describe(arguments = f"List of random sets (/help {self.command} for details)")
			async def run(interaction: discord.Interaction, arguments: str = None):

				args = []
				if arguments:
					args = arguments.split(" ")
				res = list()
				if len(args) > 0:
					for i in args:
						cur = self.parseArgs(i)
						if (int(cur[0]) < 0):
							await interaction.response.send_message(f"I cant understand your request..\nPlease look up the syntax with `/help {self.command}`!", ephemeral = True)
							return
						res.append(cur)

				embed = discord.embeds.Embed()
				embed.color = 0xEB9234
				embed.title = f"**{interaction.user.display_name}'s Roll Results**"
				file = discord.File("assets/dices.png", filename="dices.png")
				embed.set_thumbnail(url="attachment://dices.png")

				if len(args) > 0:
					for i, y in enumerate(res):
						embed.add_field(
							name = args[i],
							value = self.displayRoll(self.newRoll(y)),
							inline = True )
				else:
					embed.description = self.displayRoll(self.newRoll((1, 1, 6)))
				await interaction.response.send_message("I've noted down your results below:", file = file, embed = embed)