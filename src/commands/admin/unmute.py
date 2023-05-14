# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - unmute.py                             #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Sun May 14 17:42:08 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.core.locals import get_local
from src.utils import predicates
import discord

class Unmute:

	LOC_BASE = "command.admin.unmute"
	COMMAND = "unmute"
	ALIAS = ["demute"]
	ICON = "🔊"

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:
		registry = self.ALIAS + [self.COMMAND]
		short = self.ICON + " " + get_local("en-us", f"{self.LOC_BASE}.short")
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = short)
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
