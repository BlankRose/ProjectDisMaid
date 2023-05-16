# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - embed_clone.py                        #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Tue May 16 21:42:12 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.core.locals import get_local
from src.utils import construct, predicates
from src.core import database
import discord

class Embed_Clone:

	LOC_BASE = "command.messages.embed_clone"
	COMMAND = "embed_clone"
	ALIAS = ["embed_duplicate", "embed_dup"]
	ICON = "📟"

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:
		registry = self.ALIAS + [self.COMMAND]
		short = self.ICON + " " + get_local("en-us", f"{self.LOC_BASE}.short")
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = short)
			@discord.app_commands.describe(
				message_id = "Message which contains the embed",
				origin_channel = "Channel where is located the embed",
				target_channel = "Channel where to post the embed")
			async def run(ctx: discord.Interaction, message_id: str,
				origin_channel: discord.TextChannel = None, target_channel: discord.TextChannel = None):

				lang = database.fetch(-1, ctx.user.id).values[0]

				if await predicates.from_guild(ctx, False):
					if not await predicates.user_permissions(ctx, ctx.user, discord.Permissions(manage_messages = True)): return
					if not await predicates.app_permissions(ctx, discord.Permissions(send_messages = True)): return

				if not message_id.isdigit():
					return await construct.reply(ctx, get_local(lang, Embed_Clone.LOC_BASE + '.wrong_id'))

				if not origin_channel:
					origin_channel = ctx.channel
				if not target_channel:
					target_channel = ctx.channel

				try:
					target = await origin_channel.fetch_message(int(message_id))
				except:
					return await construct.reply(ctx, get_local(lang, Embed_Clone.LOC_BASE + '.error'))

				embed = target.embeds[0]
				if not embed:
					return await construct.reply(ctx, get_local(lang, Embed_Clone.LOC_BASE + '.no_embed'))

				await target_channel.send(embed = embed)
				await construct.reply(ctx)