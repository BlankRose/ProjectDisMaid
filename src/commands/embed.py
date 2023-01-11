import discord
from src.core import construct, predicates

class Embed():

	command = "embed"
	alias = []

	syntax = command + " [Title] [Description] [Color]"
	icon = "📟"

	short = icon + " Creates a freshly new embed"
	description = \
"""
Creates a freshly new basic embed anywhere with whichever content \
you wish, which can be further edited later using the command \
`embed_edit`, which gives even more controls over the design.

__ARGUMENTS:__
`Title` - *Text of the embed's header*
`Description` - *Content of the embed's body*
`Color` - *The color of the embed's sidebar, defined in Hexadecimal*

__UNSPECIFIED VALUES:__
`Title` - *Wont print anything but MUST be set if Description isn't*
`Description` - *Wont print anything but MUST be set if Title isn't*
`Color` - *Will give the default color*

__SIDE NOTES:__
Due to discord's limitations, embeds has their set limits as such:
 - `Titles` are limited to **256** characters
 - `Descriptions` are limited to **4096** characters
 - `Embeds` can only contains up to **25** fields
 - `Fields titles` are limited to **256** characters
 - `Fields descriptions` are limited to **1024** characters
 - `Footers` are limited to **2048** characters
 - `Author name` is limited to **256** characters
 - Finally, the total amount of characters cannot exceed **6000**

__REQUIERED PERMISSIONS:__
Application: `Send Messages`
Caller: `Manage Messages`
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

				if await predicates.from_guild(interaction, False):
					if not await predicates.user_permissions(interaction, interaction.user, discord.Permissions(manage_messages = True)): return
					if not await predicates.app_permissions(interaction, discord.Permissions(send_messages = True)): return

				if not title and not description:
					await interaction.response.send_message("You need to specify atleast a title OR a description!", ephemeral = True)
					return

				if (title and len(title) > 256) or (description and len(description) > 4096):
					await interaction.response.send_message("Due to discord's limitations, Titles are limited to 256 characters and Descriptions are limited to 4096!", ephemeral = True)
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