# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - debug.py                              #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Tue Mar  7 18:47:14 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

import discord
from src.utils import construct

class Debug():

	command = "debug"
	alias = []

	syntax = command
	icon = "⚠️"

	short = icon + " Testing purpose command"
	description = \
"""
Testing purpose command..
This is usually unstable and may not responds \
due to internal errors (but atleast it is protected)

__ARGUMENTS:__
`None` - *Doesn't contains any arguments*

__REQUIERED PERMISSIONS:__
Application: `None`
Caller: `None`
"""

	#==-----==#

	class Selector(discord.ui.View):

		options = ["A", "B", "C"]

		def __init__(self, ctx: discord.Interaction, *, timeout: float = 180):
			super().__init__(timeout=timeout)
			self.ctx = ctx

		@discord.ui.select(options=[discord.SelectOption(label = x) for x in options])
		async def callback(self, ctx: discord.Interaction, select: discord.ui.Select):
			await self.ctx.edit_original_response(content = f"Selected: {select.values[0]}")
			await ctx.response.send_message("Updated!", delete_after = 0)

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:
		registry = self.alias + [self.command]
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = self.short)
			async def run(ctx: discord.Interaction):

				if ctx.user.id != 353435819924652043:
					return await construct.reply(ctx, "I may only allow my Owner to ask me to do this dangerous task!")
				await ctx.response.send_message("Selector debug:", view = Debug.Selector(ctx), ephemeral = True)