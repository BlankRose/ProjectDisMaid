from src.core import predicates, construct
import time as t
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
					`DM` - *Will be treated as* `True`\n
					SIDE NOTES:
					`Time` can be set as following `.y.d.h.m.s` (where dots are numbers)
					`Time` can also be set to `inf` for long term mute
					By default, this command will use discord's timeout feature but this
					one is limited to 28 days by the API! This behavior can be switch to
					role-based which allows much longer mute timespan (currently WIP)"""

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

				if interaction.client.user == user:
					await interaction.response.send_message("Why do you want me silenced so badly? ;w;'", ephemeral = True)
					return

				if not await predicates.from_guild(interaction): return
				if not await predicates.is_member(interaction, user): return
				if not await predicates.user_permissions(interaction, user, discord.Permissions(moderate_members = True)): return
				if not await predicates.app_permissions(interaction, discord.Permissions(moderate_members = True)): return

				if interaction.user == user:
					await interaction.response.send_message("I don't think I can mute you.. But why would you mute yourself?", ephemeral = True)
					return

				target = interaction.guild.get_member(user.id)
				tz = construct.parse_time(time)
				if not tz:
					await interaction.response.send_message(f"Couldn't parse the given time: {time}!", ephemeral = True)
					return
				limit = construct.parse_time("28d")
				if tz > limit: tz = limit
				try: await target.timeout(tz)
				except:
					await interaction.response.send_message("I couldn't mute the targetted user!", ephemeral = True)
					return

				if dm:
					channel = await user.create_dm()
					if reason:
						await channel.send(f"You has been muted in {interaction.guild.name} until <t:{int(t.mktime(tz.timetuple()))}:R> for the following reason:\n{reason}")
					else:
						await channel.send(f"You has been muted in {interaction.guild.name} until <t:{int(t.mktime(tz.timetuple()))}:R>")
				await interaction.response.send_message(f"User {user.mention} has been successfully muted until <t:{int(t.mktime(tz.timetuple()))}:R>!", ephemeral = True)