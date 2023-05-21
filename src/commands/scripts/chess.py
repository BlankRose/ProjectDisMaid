# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - chess.py                              #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Sun May 21 19:58:21 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

import src.core.localizations as lz
import discord

class Chess:

	LOC_BASE = "command.scripts.chess"
	COMMAND = "chess"
	ALIAS = []
	ICON = '♟'

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:

		registry = self.ALIAS + [self.COMMAND]
		short = self.ICON + " " + lz.get_local(lz.FALLBACK, f"{self.LOC_BASE}.short")
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = short)
			async def run(ctx: discord.Interaction, arg1: str, arg2: str):

				lang = lz.get_userlang(ctx.user.id)
				await ctx.response.send_message(lz.get_local(lang, 'system.wip'), ephemeral = True)
