# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - random.py                             #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Wed May 17 17:59:52 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

import numpy as np
import src.core.localizations as lz
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

		try:
			if int(max) < int(min):
				tmp = max
				max = min
				min = tmp
			ret: tuple[int, int, int] = (int(rolls), int(min), int(max))
		except:
			return (-1, 0, 0)

		if ret[2] > Random.MAX_VALUE or ret[1] < Random.MIN_VALUE:
			return (-1, 0, 0)
		return ret

	#==-----==#

	def newRoll(self, args: tuple[int, int, int]) -> np.ndarray:
		""" Roll with given tuple (rolls, min, max) and returns a list of values """
		return np.random.randint(args[1], args[2] + 1, args[0])

	#==-----==#

	def displayRoll(self, values: np.ndarray, lang: str) -> str:
		""" Converts a list of values into a displayable string """

		display = str("")
		if values.size <= 50:

			if values.size > 1:
				display += lz.get_local(lang, self.LOC_BASE + '.multiple')
			else:
				display += lz.get_local(lang, self.LOC_BASE + '.single')
			display += ' '

			first = bool(True)
			for i in values:
				if first:
					display += str(i)
					first = False
				else:
					display += ", " + str(i)
				if len(display) > 200:
					display = lz.get_local(lang, self.LOC_BASE + '.too_many')
					break
		else:
			display = lz.get_local(lang, self.LOC_BASE + '.too_many')

		if values.size > 1:
			display += f"\n{lz.get_local(lang, self.LOC_BASE + '.total')} " + str(np.sum(values))
			display += f"\n{lz.get_local(lang, self.LOC_BASE + '.average')} " + str(round(np.average(values), 2))
		return display

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:
		registry = self.ALIAS + [self.COMMAND]
		short = self.ICON + " " + lz.get_local(lz.FALLBACK, f"{self.LOC_BASE}.short")
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = short)
			@discord.app_commands.describe(arguments = f"List of random sets (/help {self.COMMAND} for details)")
			async def run(ctx: discord.Interaction, arguments: str = None):

				await ctx.response.defer(ephemeral = True, thinking = True)
				lang = lz.get_userlang(ctx.user.id)

				total_rolls: int = 0
				args: list[str] = []
				if arguments:
					args = arguments.split(" ")
				res: list[tuple[int, int, int]] = [(-1, 0, 0)] * len(args)
				if len(args) > 0:
					for i, v in enumerate(args):
						res[i] = self.parseArgs(v)
						if res[i][0] < 0:
							return await ctx.followup.send(lz.get_local(lang, self.LOC_BASE + '.request', self.COMMAND))
						total_rolls += res[i][0]

				if total_rolls > Random.MAX_ROLLS:
					return await ctx.followup.send(lz.get_local(lang, self.LOC_BASE + '.limited', Random.MAX_ROLLS, total_rolls))

				embed = discord.embeds.Embed()
				embed.color = 0xEB9234
				embed.title = lz.get_local(lang, self.LOC_BASE + '.title', ctx.user.display_name)
				file = discord.File("assets/dices.png", filename="dices.png")
				embed.set_thumbnail(url="attachment://dices.png")

				if len(args) > 0:
					for i, v in enumerate(res):
						embed.add_field(
							name = args[i],
							value = self.displayRoll(self.newRoll(v), lang),
							inline = True )
				else:
					embed.description = self.displayRoll(self.newRoll((1, 1, 6)), lang)
				await ctx.followup.send(lz.get_local(lang, self.LOC_BASE + '.success'), file = file, embed = embed)
