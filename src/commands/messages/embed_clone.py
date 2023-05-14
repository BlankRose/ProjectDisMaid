# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - embed_clone.py                        #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Sun May 14 17:12:53 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.core.locals import get_local
from src.utils import construct, predicates
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

				if await predicates.from_guild(ctx, False):
					if not await predicates.user_permissions(ctx, ctx.user, discord.Permissions(manage_messages = True)): return
					if not await predicates.app_permissions(ctx, discord.Permissions(send_messages = True)): return

				if not message_id.isdigit():
					return await construct.reply(ctx, "The message ID doesn't actually looks like an ID.. It should be composed for digits!")

				if not origin_channel:
					origin_channel = ctx.channel
				if not target_channel:
					target_channel = ctx.channel

				try:
					target = await origin_channel.fetch_message(int(message_id))
				except:
					return await construct.reply(ctx, "I couldnt fetch the given message! Are you sure its the right Channel and ID?..")

				embed = target.embeds[0]
				if not embed:
					return await construct.reply(ctx, "The specified message doesn't contains any embed! You can create one with `/embed`.")

				await target_channel.send(embed = embed)
				await construct.reply(ctx)