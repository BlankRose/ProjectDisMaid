# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - embed_clone.py                        #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Tue Mar  7 17:15:51 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

import discord
from src.utils import construct, predicates

class Embed_Clone():

	command = "embed_clone"
	alias = ["embed_duplicate", "embed_dup"]

	syntax = command + " <Message ID> [Origin Channel] [Target Channel]"
	icon = "📟"

	short = icon + " Duplicates an already existing embed"
	description = \
"""
Duplicates an already existing embed into another in the same channel \
or in another channel. This tool can be used as a way in case you prepared \
the embed in a test channel and wants to exports it in a public channel or \
if you wanna modify it without changing the original.

__ARGUMENTS:__
`Message ID` - *Message which contains the embed to duplicate*
`Origin Channel` - *Channel where is located the embed to duplicate*
`Target Channel` - *Channel where to post the new embed*

__UNSPECIFIED VALUES:__
`Channel` - *Will search / post the embed in the current channel*

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