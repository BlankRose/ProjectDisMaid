# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - help.py                               #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Tue Mar  7 15:40:53 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

from typing import List
from src.commands import *
import discord

class Help():

	command = "help"
	alias = ["commands", "guidelines", "cmds"]

	syntax = command + " [Command]"
	icon = "📕"

	short = icon + " The maid's guidelines"
	description = \
"""
This command will open the maid's guidelines, where is located the \
`command` when specified or gives a summary if nothing is given.

__ARGUMENTS:__
`Command` - *Search for a specefic command*

__UNSPECIFIED VALUES:__
`Command` - *It will instead opens a summary of avaible commands*

__REQUIERED PERMISSIONS:__
Application: `None`
Caller: `None`
"""

	#==-----==#

	class Selector(discord.ui.View):

		def __init__(self, *, timeout: float = 180):
			super().__init__(timeout=timeout)

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:

		async def autocomplete(ctx: discord.Interaction, current: str) -> List[discord.app_commands.Choice[str]]:
			return [
				discord.app_commands.Choice(name = entry, value = entry)
				for entry in entries if current.lower() in entry.lower()
			]

		registry = self.alias + [self.command]
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = self.short)
			@discord.app_commands.describe(command = "The command to check")
			@discord.app_commands.autocomplete(command = autocomplete)
			async def run(ctx: discord.Interaction, command: str = None):
				embed = discord.embeds.Embed()
				embed.color = 0xb842ae
				embed.title = "**Maids' Guidelines**"
				embed.set_footer(text = "Edited by Rosie#4721 - 2022", icon_url = "https://i.imgur.com/w1BwX4h.png")

				if not command:
					file_logo = discord.File("assets/logo.png", filename = "logo.png")
					embed.description = "*Coming soon.. TM*"
					embed.set_thumbnail(url="attachment://logo.png")
					for i in entries:
						entry = entries[i]()
						embed.add_field(
							name = f"/{entry.syntax}",
							value = entry.short,
							inline = False )
					await ctx.response.send_message("Here a list of commands you can do with me:", file = file_logo, embed = embed, ephemeral = True)

					selector = discord.ui.Select()
					selector.add_option(label = "System Messages", value = "messages", description = "Commands to control system messages handled by the maid", emoji = "📟")
					view = discord.ui.View()
					view.add_item(selector)

				else:
					for i in entries:
						if i == command:
							entry = entries[i]()
							embed.description = f"{entry.icon} __**/{entry.syntax}:**__"
							if entry.alias and len(entry.alias) > 0:
								embed.description += "\n__Aliases:__"
								for i in entry.alias:
									embed.description += f" `{i}`"
							if entry.description and len(entry.description) > 0:
								embed.description += f"\n{entry.description}"
							await ctx.response.send_message("Here is what I found:", embed = embed, ephemeral = True)
							break
					else:
						await ctx.response.send_message("Sorry, I didn't found any entry in the guidelines.", ephemeral = True)