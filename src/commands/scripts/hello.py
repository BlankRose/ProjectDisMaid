# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - hello.py                              #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Wed May 17 17:18:59 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

import random as rng
from src.utils import construct
import src.core.localizations as lz
import discord

class Hello:

	LOC_BASE = "command.scripts.hello"
	COMMAND = "hello"
	ALIAS = ["hai"]
	ICON = "💬"

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:
		registry = self.ALIAS + [self.COMMAND]
		short = self.ICON + " " + lz.get_local(lz.FALLBACK, f"{self.LOC_BASE}.short")
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = short)
			async def run(ctx: discord.Interaction):
				lang = lz.get_userlang(ctx.user.id)

				caseA = lz.get_local(lang, self.LOC_BASE + '.first').split('\n')
				strA = caseA[rng.randrange(0, len(caseA))]
				caseB = lz.get_local(lang, self.LOC_BASE + '.second').split('\n')
				strB = caseB[rng.randrange(0, len(caseB))]
				await construct.reply(ctx, f"{strA}\n{strB}")