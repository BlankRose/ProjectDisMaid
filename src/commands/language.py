# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - language.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Wed May 17 18:08:59 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.core import \
	localizations as lz, \
	database as db
import discord

class Language:

	LOC_BASE = "command.general.language"
	COMMAND = "language"
	ALIAS = ["localization", "local", "lang"]
	ICON = "🌐"

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:

		async def autocomplete(_: discord.Interaction, current: str):
			return [
				discord.app_commands.Choice(name = entry, value = entry)
				for entry in lz.available if current.lower() in entry.lower()
			]

		registry = self.ALIAS + [self.COMMAND]
		short = self.ICON + " " + lz.get_local(lz.FALLBACK, f"{self.LOC_BASE}.short")
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = short)
			@discord.app_commands.describe(language = "Localization to use")
			@discord.app_commands.autocomplete(language = autocomplete)
			async def run(ctx: discord.Interaction, language: str):

				if language.lower() not in lz.available:
					await ctx.response.send_message("Sorry, this language is unavailable :(", ephemeral = True)
					return

				db.store(-1, ctx.user.id, language, 'lang')
				await ctx.response.send_message(lz.get_local(language, f"{Language.LOC_BASE}.success"), ephemeral = True)
