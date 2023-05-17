# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - mute.py                               #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Wed May 17 14:11:52 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

import time as t
from src.utils import predicates, construct
import src.core.localizations as lz
import discord

class Mute:

	LOC_BASE = "command.admin.mute"
	COMMAND = "mute"
	ALIAS = ["silence", "timeout"]
	ICON = "🔇"

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:
		registry = self.ALIAS + [self.COMMAND]
		short = self.ICON + " " + lz.get_local(lz.FALLBACK, f"{self.LOC_BASE}.short")
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = short)
			@discord.app_commands.describe(
				user = "User to mute",
				time = "Mute duration",
				reason = "Reason of the mute",
				dm = "Wether or not a notification should be sent")
			async def run(ctx: discord.Interaction, user: discord.User, time: str, reason: str = None, dm: bool = True):
				lang = lz.get_userlang(ctx.user.id)

				if ctx.client.user == user:
					await ctx.response.send_message(lz.get_local(lang, self.LOC_BASE + '.maid'), ephemeral = True)
					return

				if not await predicates.from_guild(ctx, lang): return
				if not await predicates.is_member(ctx, user, lang): return
				if not await predicates.user_permissions(ctx, user, discord.Permissions(moderate_members = True), lang): return
				if not await predicates.app_permissions(ctx, discord.Permissions(moderate_members = True), lang): return

				if ctx.user == user:
					await ctx.response.send_message(lz.get_local(lang, self.LOC_BASE + '.self'), ephemeral = True)
					return

				target = ctx.guild.get_member(user.id)
				tz = construct.parse_time(time)
				if not tz:
					await ctx.response.send_message(lz.get_local(lang, self.LOC_BASE + '.time', time), ephemeral = True)
					return
				limit = construct.parse_time("28d")
				if tz > limit: tz = limit
				try: await target.timeout(tz)
				except:
					await ctx.response.send_message(lz.get_local(lang, self.LOC_BASE + '.fail'), ephemeral = True)
					return

				time_display = f"<t:{int(t.mktime(tz.timetuple()))}:R>"
				if dm:
					user_lang = lz.get_userlang(user.id)
					channel = await user.create_dm()
					msg = lz.get_local(user_lang, self.LOC_BASE + '.dm_base', ctx.guild.name, time_display)
					if reason:
						msg += lz.get_local(user_lang, self.LOC_BASE + '.dm_reason', reason)
					await channel.send(msg)
				await ctx.response.send_message(lz.get_local(lang, self.LOC_BASE + '.success', user.mention, time_display), ephemeral = True)