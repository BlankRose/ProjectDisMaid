# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - template.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Fri Mar 10 21:02:36 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

import discord

class T:

	COMMAND = ""
	ALIAS = []

	SYNTAX = COMMAND
	ICON = ""

	SHORT = ICON + " "
	DESCRIPTION = \
"""
... Here goes description ...

__ARGUMENTS:__
`None` - *Doesn't contains any arguments*

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
			async def run(ctx: discord.Interaction):
				await ctx.response.send_message("How did we get here..?", ephemeral = True)