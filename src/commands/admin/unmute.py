# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - unmute.py                             #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Wed May 17 16:58:37 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.utils import predicates
import src.core.localizations as lz
import discord

class Unmute:

	LOC_BASE = "command.admin.unmute"
	COMMAND = "unmute"
	ALIAS = ["demute"]
	ICON = "🔊"

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:
		registry = self.ALIAS + [self.COMMAND]
		short = self.ICON + " " + lz.get_local(lz.FALLBACK, f"{self.LOC_BASE}.short")
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = short)
			@discord.app_commands.describe(
				user = "User to unmute",
				dm = "Wether or not a notification should be sent")
			async def run(ctx: discord.Interaction, user: discord.User, dm: bool = True):
				lang = lz.get_userlang(ctx.user.id)

				if not await predicates.from_guild(ctx, lang): return
				if not await predicates.is_member(ctx, user, lang): return
				if not await predicates.user_permissions(ctx, ctx.user, discord.Permissions(moderate_members = True), lang): return
				if not await predicates.app_permissions(ctx, discord.Permissions(moderate_members = True), lang): return

				target = ctx.guild.get_member(user.id)
				try: await target.timeout(None)
				except:
					await ctx.response.send_message(lz.get_local(lang, self.LOC_BASE + '.fail'), ephemeral = True)
					return

				if dm:
					channel = await user.create_dm()
					user_lang = lz.get_userlang(user.id)
					await channel.send(lz.get_local(user_lang, self.LOC_BASE + '.dm', ctx.guild.name))
				await ctx.response.send_message(lz.get_local(lang, self.LOC_BASE + 'success', user.mention), ephemeral = True)
