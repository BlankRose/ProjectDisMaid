import discord

class T():

	command = ""
	alias = []

	syntax = command
	icon = ""

	short = icon + " "
	description = """...\n
					ARGUMENTS:
					`None` - *Doesn't contains any arguments*"""

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:
		registry = self.alias + [self.command]
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = self.short)
			async def run(interaction: discord.Interaction):
				await interaction.response.send_message("How did we get here..?", ephemeral = True)