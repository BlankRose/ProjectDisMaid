# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - mute.py                               #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Mon Mar  6 17:09:31 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.core import predicates, construct
import time as t
import discord

class Mute():

	command = "mute"
	alias = ["silence", "timeout"]

	syntax = command + " <User> [Time] [Reason] [DM]"
	icon = "🔇"

	short = icon + " Silence anyone who is being nasty"
	description = \
"""
A basic command to mute someone with some extra parameters to \
work around. We hope muting can calm those nasty poeple..

__ARGUMENTS:__
`User` - *User to target (dont try on me plz)*
`Time` - *How long they shall be muted*
`Reason` - *Why do you want to mute them*
`DM` - *Wether or not we shall notify the user in their DMs*

__UNSPECIFIED VALUES:__
`Time` - *Will be treated as* `inf`
`DM` - *Will be treated as* `True`

__SIDE NOTES:__
`Time` can be set as following `.y.d.h.m.s` (where dots are numbers)
`Time` can also be set to `inf` for long term mute
By default, this command will use discord's timeout feature but this \
one is limited to 28 days by the API! This behavior can be switch to \
role-based which allows much longer mute timespan (currently WIP)

__REQUIERED PERMISSIONS:__
Application: `Moderate Members`
Caller: `Moderate Members`
"""

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:
		registry = self.alias + [self.command]
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = self.short)
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