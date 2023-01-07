import discord

class Print():

	command = "print"
	alias = []

	syntax = command
	icon = "👾"

	short = icon + " DEV - Prints out various stuff"
	description = """Prints out any desired stuff made the dev\n
					ARGUMENTS:
					`None` - *Doesn't contains any arguments*\n
					DEV-Only command!"""

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:
		registry = self.alias + [self.command]
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = self.short)
			async def run(interaction: discord.Interaction):

				a = discord.Embed(
					title = "\t---==[  RULES  ]==---",
					color = 0xFF0000,
					description = "...\n"
				)

				a.add_field(
					name = "**[ 1 ]** __Everyone should be respected__",
					value = "...",
					inline = False
				)

				a.add_field(
					name = "**[ 2 ]** __Keep the topics in the respective channels__",
					value = "...",
					inline = False
				)

				await interaction.channel.send(embed = a)
				await interaction.response.send_message("Done!", delete_after = .001, ephemeral = True)