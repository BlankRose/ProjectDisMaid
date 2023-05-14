# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - embed.py                              #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Sun May 14 17:39:40 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.core.locals import get_local
from src.utils import construct, predicates
import discord

class Embed:

	LOC_BASE = "command.messages.embed"
	COMMAND = "embed"
	ALIAS = []
	ICON = "📟"

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:
		registry = self.ALIAS + [self.COMMAND]
		short = self.ICON + " " + get_local("en-us", f"{self.LOC_BASE}.short")
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = short)
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