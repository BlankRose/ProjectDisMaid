import discord
import random as rng

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
			async def run(interaction: discord.Interaction):
				caseA = ["Hai sweetheart~",
						"Hello there~",
						"Hoi!"]
				strA = caseA[rng.randrange(0, len(caseA))]
				caseB = ["(^owo^)s *Meow.*",
						"How are you?",
						"Would you like some cookies?",
						"Have you seen my cat? I can't find it anywhere."]
				strB = caseB[rng.randrange(0, len(caseB))]
				await interaction.response.send_message(f"{strA}\n{strB}", ephemeral=True)