import discord
from src.core import construct

class Embed():

	command = "embed"
	alias = []

	syntax = command + " [Title] [Description] [Color]"
	icon = "📟"

	short = icon + " Creates a freshly new embed"
	description = """Creates a freshly new basic embed anywhere with whichever content
					you wish, which can be further edited later using the command
					`embed_edit`, which gives even more controls over the design.\n
					ARGUMENTS:
					`Title` - *Text of the embed's header*
					`Description` - *Content of the embed's body*
					`Color` - *The color of the embed's sidebar, defined in Hexadecimal*\n
					UNSPECIFIED VALUES:
					`Title` - *Wont print anything but MUST be set if Description isn't*
					`Description` - *Wont print anything but MUST be set if Title isn't*
					`Color` - *Will give the default color*\n
					"""

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:
		registry = self.alias + [self.command]
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = self.short)
			@discord.app_commands.describe(
				title = "Title of the embed",
				description = "Description of the embed",
				color = "Color of the embed in hexadecimal")
			async def run(interaction: discord.Interaction, title: str = None, description: str = None, color: str = None):

				if not title and not description:
					await interaction.response.send_message("You need to specify atleast a title OR a description!", ephemeral = True)
					return

				res = None
				if color:
					if len(color) <= 6:
						res = construct.parse_hexa(color)
						if not res:
							await interaction.response.send_message("Invalid color code given in parameter!", ephemeral = True)
					else:	await interaction.response.send_message("Color value must be at maximum 6 character long!", ephemeral = True)

				a = discord.Embed(
					title = title,
					description = description,
					color = res
				)

				await interaction.channel.send(embed = a)
				await interaction.response.send_message("Done!", delete_after = .001, ephemeral = True)