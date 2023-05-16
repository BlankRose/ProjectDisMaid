# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - embed.py                              #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Tue May 16 21:33:29 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.core.locals import get_local
from src.utils import construct, predicates
from src.core import database
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

				lang = database.fetch(-1, ctx.user.id).values[0]

				if await predicates.from_guild(ctx, False):
					if not await predicates.user_permissions(ctx, ctx.user, discord.Permissions(manage_messages = True)): return
					if not await predicates.app_permissions(ctx, discord.Permissions(send_messages = True)): return

				if not title and not description:
					await construct.reply(ctx, get_local(lang, Embed.LOC_BASE + '.empty'))
					return

				if (title and len(title) > 256) or (description and len(description) > 4096):
					await construct.reply(ctx, get_local(lang, Embed.LOC_BASE + '.limited'))
					return

				res = None
				if color:
					if len(color) <= 6:
						res = construct.parse_hexa(color)
						if not res:
							await construct.reply(ctx, get_local(lang, Embed.LOC_BASE + '.color_invalid'))
					else: await construct.reply(ctx, get_local(lang, Embed.LOC_BASE + '.color_long'))

				new_embed = discord.Embed(
					title = title,
					description = description,
					color = res
				)

				if channel:	await channel.send(embed = new_embed)
				else:		await ctx.channel.send(embed = new_embed)
				await construct.reply(ctx)