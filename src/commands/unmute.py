# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - unmute.py                             #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Tue Mar  7 17:14:20 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.utils import predicates
import discord

class Unmute():

	command = "unmute"
	alias = ["demute"]

	syntax = command + " <User> [DM]"
	icon = "🔊"

	short = icon + " Lift off any silence punishments"
	description = \
"""
A basic command to unmute someone, giving them back the right \
to talk. Did the mute finally calmed them down?

__ARGUMENTS:__
`User` - *User to target*
`DM` - *Wether or not we shall notify the user in their DMs*

__UNSPECIFIED VALUES:__
`DM` - *Will be treated as* `True`

__SIDE NOTES:__
If you went for role-based mutes and have changed to a different \
roles, members who has been muted before hand might be still \
muted. So watch out for that in case you can't unmute them!

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
				user = "User to unmute",
				dm = "Wether or not a notification should be sent")
			async def run(ctx: discord.Interaction, user: discord.User, dm: bool = True):

				if not await predicates.from_guild(ctx): return
				if not await predicates.is_member(ctx, user): return
				if not await predicates.user_permissions(ctx, ctx.user, discord.Permissions(moderate_members = True)): return
				if not await predicates.app_permissions(ctx, discord.Permissions(moderate_members = True)): return

				target = ctx.guild.get_member(user.id)
				try: await target.timeout(None)
				except:
					await ctx.response.send_message("I couldn't unmute the targetted user!", ephemeral = True)
					return

				if dm:
					channel = await user.create_dm()
					await channel.send(f"Your timeout has been lifted in {ctx.guild.name}!")
				await ctx.response.send_message(f"User {user.mention} has been successfully unmuted!", ephemeral = True)
