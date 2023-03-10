# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - help.py                               #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Fri Mar 10 21:06:21 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.commands import *
import logging as logs
import discord

class Help():

	COMMAND = "help"
	ALIAS = ["commands", "guidelines", "cmds"]

	SYNTAX = COMMAND + " [Command]"
	ICON = "📕"

	SHORT = ICON + " The maid's guidelines"
	DESCRIPTION = \
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

		options: list = [
			discord.SelectOption(
				label = category_details[x]().TITLE,
				description = category_details[x]().DESCRIPTION,
				emoji = category_details[x]().ICON,
				value = x)
			for x in categories]

		def __init__(self, ctx: discord.Interaction, base: discord.Embed, *, timeout: float = 180):
			super().__init__(timeout = timeout)
			self.origin = ctx
			self.embed = base

		@discord.ui.select(options = options, placeholder = "More commands...")
		async def callback(self, ctx: discord.Interaction, select: discord.ui.Select):
			from src.commands import sub_entries

			target = sub_entries[select.values[0]]
			self.embed.clear_fields()
			self.embed.description = None

			for i in target:
				entry = target[i]()
				self.embed.add_field(
					name = f"/{entry.SYNTAX}",
					value = entry.SHORT,
					inline = False )

			await self.origin.edit_original_response(content = f"Here's the commands for the {select.values[0]} category:", embed = self.embed)
			await ctx.response.send_message("Updated!", delete_after = 0)

		async def on_timeout(self) -> None:
			try:
				res = (await self.origin.original_response())
				await res.edit(content = f"⚠️ *This interaction has timed out!*\n{res.content}", view = None)
			except Exception as err:
				logs.error(err)
			return await super().on_timeout()

		async def on_error(self, ctx: discord.Interaction, error: Exception, item, /) -> None:
			await ctx.response("I'm sorry, an problem occured while trying to handle your request..")
			return await super().on_error(ctx, error, item)

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:

		async def autocomplete(_: discord.Interaction, current: str):
			return [
				discord.app_commands.Choice(name = entry, value = entry)
				for entry in entries if current.lower() in entry.lower()
			]

		registry = self.ALIAS + [self.COMMAND]
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = self.SHORT)
			@discord.app_commands.describe(command = "The command to check")
			@discord.app_commands.autocomplete(command = autocomplete)
			async def run(ctx: discord.Interaction, command: str = None):

				embed = discord.embeds.Embed()
				embed.color = 0xb842ae
				embed.title = "**Maids' Guidelines**"
				embed.set_footer(text = "Edited by Rosie#4721 - 2022", icon_url = "https://i.imgur.com/w1BwX4h.png")

				if not command:

					for i in entries:
						if i in non_categorized:
							entry = entries[i]()
							embed.add_field(
								name = f"/{entry.SYNTAX}",
								value = entry.SHORT,
								inline = False )

					embed.add_field(
						name = "",
						value = "To view commands, please use the selector below.",
						inline = False )

					from src.core.client import Client
					embed.description = Client.DESCRIPTION

					file_logo = discord.File("assets/logo.png", filename = "logo.png")
					embed.set_thumbnail(url="attachment://logo.png")
					await ctx.response.send_message("Here a list of commands you can do with me:", file = file_logo, embed = embed, ephemeral = True, view = Help.Selector(ctx, embed))

				else:

					if command in entries:
						entry: Any = entries[command]()
						embed.description = f"{entry.ICON} __**/{entry.SYNTAX}:**__"
						if entry.ALIAS and len(entry.ALIAS) > 0:
							embed.description += "\n__Aliases:__"
							for i in entry.ALIAS:
								embed.description += f" `{i}`"
						if entry.DESCRIPTION and len(entry.DESCRIPTION) > 0:
							embed.description += f"\n{entry.DESCRIPTION}"
						await ctx.response.send_message("Here is what I found:", embed = embed, ephemeral = True)
					else:
						await ctx.response.send_message("Sorry, I didn't found any entry in the guidelines.", ephemeral = True)