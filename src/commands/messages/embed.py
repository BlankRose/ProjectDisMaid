# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - embed.py                              #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Fri Mar 10 20:53:11 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

import discord
from src.utils import construct, predicates

class Embed():

	COMMAND = "embed"
	ALIAS = []

	SYNTAX = COMMAND + " [Channel] [Title] [Description] [Color]"
	ICON = "📟"

	SHORT = ICON + " Creates a freshly new embed"
	DESCRIPTION = \
"""
Creates a freshly new basic embed anywhere with whichever content \
you wish, which can be further edited later using the command \
`embed_edit`, which gives even more controls over the design.

__ARGUMENTS:__
`Channel` - *Channel where to post the new embed*
`Title` - *Text of the embed's header*
`Description` - *Content of the embed's body*
`Color` - *The color of the embed's sidebar, defined in Hexadecimal*

__UNSPECIFIED VALUES:__
`Channel` - *Will post the embed in the current channel*
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
		registry = self.ALIAS + [self.COMMAND]
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = self.SHORT)
			@discord.app_commands.describe(
				title = "Title of the embed",
				description = "Description of the embed",
				color = "Color of the embed in hexadecimal")
			async def run(ctx: discord.Interaction, channel: discord.TextChannel = None, title: str = None, description: str = None, color: str = None):

				if await predicates.from_guild(ctx, False):
					if not await predicates.user_permissions(ctx, ctx.user, discord.Permissions(manage_messages = True)): return
					if not await predicates.app_permissions(ctx, discord.Permissions(send_messages = True)): return

				if not title and not description:
					await construct.reply(ctx, "You need to specify atleast a title OR a description!")
					return

				if (title and len(title) > 256) or (description and len(description) > 4096):
					await construct.reply(ctx, "Due to discord's limitations, Titles are limited to 256 characters and Descriptions are limited to 4096!")
					return

				res = None
				if color:
					if len(color) <= 6:
						res = construct.parse_hexa(color)
						if not res:
							await construct.reply(ctx, "Invalid color code given in parameter!")
					else:	await construct.reply(ctx, "Color value must be at maximum 6 character long!")

				new_embed = discord.Embed(
					title = title,
					description = description,
					color = res
				)

				if channel:	await channel.send(embed = new_embed)
				else:		await ctx.channel.send(embed = new_embed)
				await construct.reply(ctx)