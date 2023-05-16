# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - level.py                              #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Tue May 16 21:56:09 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.core.locals import get_local
from src.core import database
import discord

class Level:

	LOC_BASE = "command.data.level"
	COMMAND = "level"
	ALIAS = ["lvl", "rank", "stats"]
	ICON = "⬆️"

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:
		registry = self.ALIAS + [self.COMMAND]
		short = self.ICON + " " + get_local("en-us", f"{self.LOC_BASE}.short")
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = short)
			async def run(ctx: discord.Interaction, user: discord.User = None):

				lang = database.fetch(-1, ctx.user.id).values[0]
				await ctx.response.send_message(get_local(lang, 'system.wip'), ephemeral = True)