# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - help.py                               #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Sun May 14 19:20:08 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.core.locals import get_local
from src.utils import construct
from src.commands import *
import logging as logs
import discord

class Help:

	LOC_BASE = "command.general.help"
	COMMAND = "help"
	ALIAS = ["commands", "guidelines", "cmds"]
	ICON = "📕"

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
				syntax = get_local("en-us", f"{entry.LOC_BASE}.syntax")
				short = get_local("en-us", f"{entry.LOC_BASE}.short")

				self.embed.add_field(
					name = f"/{entry.COMMAND} {syntax}",
					value = f"{entry.ICON} {short}",
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
		short = self.ICON + " " + get_local("en-us", f"{self.LOC_BASE}.short")
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = short)
			@discord.app_commands.describe(command = "The command to check")
			@discord.app_commands.autocomplete(command = autocomplete)
			async def run(ctx: discord.Interaction, command: str = None):

				# Base Embed Structure
				embed = discord.embeds.Embed()
				embed.color = 0xb842ae
				embed.title = "**Maids' Guidelines**"
				embed.set_footer(text = "Edited by Rosie#4721 - 2022", icon_url = "https://i.imgur.com/w1BwX4h.png")

				# Default Behavior
				if not command:

					for i in entries:
						if i in non_categorized:
							entry = entries[i]()
							syntax = get_local("en-us", f"{entry.LOC_BASE}.syntax")
							short = get_local("en-us", f"{entry.LOC_BASE}.short")

							embed.add_field(
								name = f"/{entry.COMMAND} {syntax}",
								value = f"{entry.ICON} {short}",
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

				# Search and Display Command
				else:

					if command in entries:
						entry: Any = entries[command]()
						syntax = get_local("en-us", f"{entry.LOC_BASE}.syntax")
						description = construct.full_description("en-us", entry.LOC_BASE)

						embed.description = f"{entry.ICON} __**/{entry.COMMAND} {syntax}:**__"
						if entry.ALIAS and len(entry.ALIAS) > 0:
							embed.description += "\n__Aliases:__"
							for i in entry.ALIAS:
								embed.description += f" `{i}`"
						if description and len(description) > 0:
							embed.description += f"\n{description}"
						await ctx.response.send_message("Here is what I found:", embed = embed, ephemeral = True)
					else:
						await ctx.response.send_message("Sorry, I didn't found any entry in the guidelines.", ephemeral = True)