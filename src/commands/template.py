# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - template.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Mon Mar  6 17:09:51 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

import discord

class T():

	command = ""
	alias = []

	syntax = command
	icon = ""

	short = icon + " "
	description = \
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
		registry = self.alias + [self.command]
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = self.short)
			async def run(ctx: discord.Interaction):
				await ctx.response.send_message("How did we get here..?", ephemeral = True)