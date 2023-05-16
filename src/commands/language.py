# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - language.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Tue May 16 18:42:25 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.core import database, locals
import discord

class Language:

	LOC_BASE = "command.general.language"
	COMMAND = "language"
	ALIAS = ["lang"]
	ICON = "🌐"

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:

		async def autocomplete(_: discord.Interaction, current: str):
			return [
				discord.app_commands.Choice(name = entry, value = entry)
				for entry in locals.available if current.lower() in entry.lower()
			]

		registry = self.ALIAS + [self.COMMAND]
		short = self.ICON + " " + locals.get_local("en-us", f"{self.LOC_BASE}.short")
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = short)
			@discord.app_commands.describe(language = "Localization to use")
			@discord.app_commands.autocomplete(language = autocomplete)
			async def run(ctx: discord.Interaction, language: str):

				if language.lower() not in locals.available:
					await ctx.response.send_message("Sorry, this language is unavailable :(", ephemeral = True)
					return

				database.store(-1, ctx.user.id, language, 'lang')
				await ctx.response.send_message(locals.get_local(language, f"{Language.LOC_BASE}.success"), ephemeral = True)
