from typing import List
from src.commands import *
import discord

class Help():

	command = "help"
	alias = ["commands", "guidelines", "cmds"]

	syntax = command + " [command]"
	icon = "📕"

	short = icon + " The maid's guidelines"
	description = """This command will open the maid's guidelines, where is located the `command` when specified or gives a summary if nothing is given.\n
					ARGUMENTS :
					`COMMAND` - *Search for a specefic command*"""

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:
		registry = self.alias + [self.command]
		for i in registry:

	#==-----==#

			async def autocomplete(interaction: discord.Interaction, current: str) -> List[discord.app_commands.Choice[str]]:
				return [
					discord.app_commands.Choice(name = entry, value = entry)
					for entry in entries if current.lower() in entry.lower()
				]

	#==-----==#

			@cmd.command(name = i, description = self.short)
			@discord.app_commands.autocomplete(command = autocomplete)
			async def run(interaction: discord.Interaction, command: str = None):
				embed = discord.embeds.Embed()
				embed.color = 0xb842ae
				embed.title = "**Maids' Guidelines**"

				file_logo = discord.File("assets/logo.png", filename = "logo.png")
				if not command:
					embed.description = "*Comming soon.. TM*"
					embed.set_thumbnail(url="attachment://logo.png")
					for i in entries:
						entry = entries[i]()
						embed.add_field(
							name = f"/{entry.syntax}",
							value = entry.short,
							inline = False )
				else:
					for i in entries:
						if i == command:
							entry = entries[i]()
							embed.description = f"{entry.icon} __**/{entry.syntax}:**__\n__Aliases:__"
							for i in entry.alias:
								embed.description += f" `{i}`"
							embed.description += f"\n\n{entry.description}"
							break
					else:
						await interaction.response.send_message("Sorry, I didn't found any entry in the guidelines.", ephemeral = True)
						return

				embed.set_footer(text = "Edited by Rosie#4721 - 2022", icon_url = "https://i.imgur.com/w1BwX4h.png")
				await interaction.response.send_message("Here is what I found:", file = file_logo, embed = embed, ephemeral = True)