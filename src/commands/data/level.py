# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - level.py                              #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Sat Mar 11 21:38:42 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

import discord

class Level:

	COMMAND = "level"
	ALIAS = ["lvl", "rank", "stats"]

	SYNTAX = COMMAND + " [User]"
	ICON = "⬆️"

	SHORT = ICON + " Displays leveling statistics"
	DESCRIPTION = \
"""
Displays some detailed stats about the target's levels, \
if the leveling system is enabled within the server.

__ARGUMENTS:__
`User` - *Targetted User to show stats off*

__UNSPECIFIED VALUES:__
`User` - *It will target the caller by default*

__REQUIERED PERMISSIONS:__
Application: `None`
Caller: `None`
"""

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:
		registry = self.ALIAS + [self.COMMAND]
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = self.SHORT)
			async def run(ctx: discord.Interaction, user: discord.User = None):
				await ctx.response.send_message("How did we get here..?", ephemeral = True)