# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - hello.py                              #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Sun May 14 17:38:10 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.core.locals import get_local
from src.utils import construct
import random as rng
import discord

class Hello:

	LOC_BASE = "command.scripts.hello"
	COMMAND = "hello"
	ALIAS = ["hai"]
	ICON = "💬"

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:
		registry = self.ALIAS + [self.COMMAND]
		short = self.ICON + " " + get_local("en-us", f"{self.LOC_BASE}.short")
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = short)
			async def run(ctx: discord.Interaction):
				caseA = ["Hai sweetheart~",
						"Hello there~",
						"Hoi!"]
				strA = caseA[rng.randrange(0, len(caseA))]
				caseB = ["(^owo^)s *Meow.*",
						"How are you?",
						"Would you like some cookies?",
						"Have you seen my cat? I can't find it anywhere."]
				strB = caseB[rng.randrange(0, len(caseB))]
				await construct.reply(ctx, f"{strA}\n{strB}")