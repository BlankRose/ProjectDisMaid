# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - language.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Mon May 15 11:27:53 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.core.locals import get_local
import discord

class Language:

	LOC_BASE = "command.general.language"
	COMMAND = "language"
	ALIAS = ["lang"]
	ICON = "🌐"

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:
		registry = self.ALIAS + [self.COMMAND]
		short = self.ICON + " " + get_local("en-us", f"{self.LOC_BASE}.short")
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = short)
			async def run(ctx: discord.Interaction):
				await ctx.response.send_message("Command in progress..", ephemeral = True)