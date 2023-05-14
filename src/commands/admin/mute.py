# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - mute.py                               #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Sun May 14 17:41:51 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.core.locals import get_local
from src.utils import predicates, construct
import time as t
import discord

class Mute:

	LOC_BASE = "command.admin.mute"
	COMMAND = "mute"
	ALIAS = ["silence", "timeout"]
	ICON = "🔇"

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:
		registry = self.ALIAS + [self.COMMAND]
		short = self.ICON + " " + get_local("en-us", f"{self.LOC_BASE}.short")
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = short)
			@discord.app_commands.describe(
				user = "User to mute",
				time = "Mute duration",
				reason = "Reason of the mute",
				dm = "Wether or not a notification should be sent")
			async def run(ctx: discord.Interaction, user: discord.User, time: str, reason: str = None, dm: bool = True):

				if ctx.client.user == user:
					await ctx.response.send_message("Why do you want me silenced so badly? ;w;'", ephemeral = True)
					return

				if not await predicates.from_guild(ctx): return
				if not await predicates.is_member(ctx, user): return
				if not await predicates.user_permissions(ctx, user, discord.Permissions(moderate_members = True)): return
				if not await predicates.app_permissions(ctx, discord.Permissions(moderate_members = True)): return

				if ctx.user == user:
					await ctx.response.send_message("I don't think I can mute you.. But why would you mute yourself?", ephemeral = True)
					return

				target = ctx.guild.get_member(user.id)
				tz = construct.parse_time(time)
				if not tz:
					await ctx.response.send_message(f"Couldn't parse the given time: {time}!", ephemeral = True)
					return
				limit = construct.parse_time("28d")
				if tz > limit: tz = limit
				try: await target.timeout(tz)
				except:
					await ctx.response.send_message("I couldn't mute the targetted user!", ephemeral = True)
					return

				if dm:
					channel = await user.create_dm()
					if reason:
						await channel.send(f"You has been muted in {ctx.guild.name} until <t:{int(t.mktime(tz.timetuple()))}:R> for the following reason:\n{reason}")
					else:
						await channel.send(f"You has been muted in {ctx.guild.name} until <t:{int(t.mktime(tz.timetuple()))}:R>")
				await ctx.response.send_message(f"User {user.mention} has been successfully muted until <t:{int(t.mktime(tz.timetuple()))}:R>!", ephemeral = True)