from src.core import predicates
import discord

class Mute():

	command = "mute"
	alias = ["silence", "timeout"]

	syntax = command + " <User> [Time] [Reason] [DM]"
	icon = "🔇"

	short = icon + " Silence anyone who is being nasty"
	description = """A basic command to mute someone with some extra parameters to
					work around. We hope muting can calm those nasty poeple..\n
					ARGUMENTS:
					`User` - *User to target (dont try on me plz)*
					`Time` - *How long they shall be muted*
					`Reason` - *Why do you want to mute them*
					`DM` - *Wether or not we shall notify the user in their DMs*\n
					UNSPECIFIED VALUES:
					`Time` - *Will be treated as* `inf`
					`DM` - *Will be treated as* `True`"""

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
			async def run(interaction: discord.Interaction, user: discord.User, time: str, reason: str = None, dm: bool = True):

				if not await predicates.guild(interaction): return
				if not await predicates.user_permissions(interaction, user, discord.Permissions(moderate_members = True)): return
				if not await predicates.app_permissions(interaction, discord.Permissions(moderate_members = True)): return

				target = interaction.guild.get_member(user.id)
				if not target:
					await interaction.response.send_message("User not found!", ephemeral = True)
					return
				if dm:
					channel = await user.create_dm()
					if reason:
						await channel.send(f"You has been muted in {interaction.guild.name} for {time} for the following reason:\n{reason}")
					else:
						await channel.send(f"You has been muted in {interaction.guild.name} for {time}")
				await interaction.response.send_message("Test success!", ephemeral = True)