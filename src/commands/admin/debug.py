# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - debug.py                              #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Sun May 14 17:41:32 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.core.locals import get_local
from src.utils import construct
import discord

class Debug:

	LOC_BASE = "command.admin.debug"
	COMMAND = "debug"
	ALIAS = []
	ICON = "⚠️"

	#==-----==#

	class Selector(discord.ui.View):

		options = ["A", "B", "C"]

		def __init__(self, ctx: discord.Interaction, *, timeout: float = 180):
			super().__init__(timeout=timeout)
			self.origin = ctx

		@discord.ui.select(options=[discord.SelectOption(label = x) for x in options])
		async def callback(self, ctx: discord.Interaction, select: discord.ui.Select):
			await self.origin.edit_original_response(content = f"Selected: {select.values[0]}")
			await ctx.response.send_message("Updated!", delete_after = 0)

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:
		registry = self.ALIAS + [self.COMMAND]
		short = self.ICON + " " + get_local("en-us", f"{self.LOC_BASE}.short")
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = short)
			async def run(ctx: discord.Interaction):

				if ctx.user.id != 353435819924652043:
					return await construct.reply(ctx, "I may only allow my Owner to ask me to do this dangerous task!")
				await ctx.response.send_message("Selector debug:", view = Debug.Selector(ctx), ephemeral = True)
				await ctx.response.send_message("Should throws error...", ephemeral = True)