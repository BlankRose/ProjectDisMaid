from src.core import predicates
import time as t
import discord

class Unmute():

	command = "unmute"
	alias = ["demute"]

	syntax = command + " <User> [DM]"
	icon = "🔊"

	short = icon + " Lift off any silence punishments"
	description = """A basic command to unmute someone, giving them back the right
					to talk. Did the mute finally calmed them down?\n
					ARGUMENTS:
					`User` - *User to target*
					`DM` - *Wether or not we shall notify the user in their DMs*\n
					UNSPECIFIED VALUES:
					`DM` - *Will be treated as* `True`\n
					SIDE NOTES:
					If you went for role-based mutes and have changed to a different
					roles, members who has been muted before hand might be still
					muted. So watch out for that in case you can't unmute them!"""

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:
		registry = self.alias + [self.command]
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = self.short)
			@discord.app_commands.describe(
				user = "User to unmute",
				dm = "Wether or not a notification should be sent")
			async def run(interaction: discord.Interaction, user: discord.User, dm: bool = True):

				if not await predicates.guild(interaction): return
				if not await predicates.is_member(interaction, user): return
				if not await predicates.user_permissions(interaction, user, discord.Permissions(moderate_members = True)): return
				if not await predicates.app_permissions(interaction, discord.Permissions(moderate_members = True)): return

				target = interaction.guild.get_member(user.id)
				try: await target.timeout(None)
				except:
					await interaction.response.send_message("I couldn't unmute the targetted user!", ephemeral = True)
					return

				if dm:
					channel = await user.create_dm()
					await channel.send(f"Your timeout has been lifted in {interaction.guild.name}!")
				await interaction.response.send_message(f"User {user.mention} has been successfully unmuted!", ephemeral = True)
