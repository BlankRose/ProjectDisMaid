# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - hello.py                              #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Mon Mar  6 18:12:53 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

import discord
import random as rng
from src.utils import construct

class Hello():

	command = "hello"
	alias = ["hai"]

	syntax = command
	icon = "💬"

	short = icon + " Giving a warm welcome to the maid is always appreciable"
	description = \
"""
Giving out a warm welcome to the hard working maid is always \
appreciated and means a lot to them!~ xoxo~

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