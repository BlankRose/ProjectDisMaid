# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - help.py                               #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Tue May 16 22:09:01 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.core.locals import get_local
from src.utils import construct
from src.core import database
from src.commands import *
import logging as logs
import discord

class Help:

	LOC_BASE = "command.general.help"
	COMMAND = "help"
	ALIAS = ["commands", "guidelines", "cmds"]
	ICON = "📕"

	_tmp_options = []

	#==-----==#

	@staticmethod
	def new_selector(ctx: discord.Interaction, base: discord.Embed, lang: str, *, timeout: float = 180):

		options: list = [
			discord.SelectOption(
				label = get_local(lang, f"{category_details[x]().LOC_BASE}.title"),
				description = get_local(lang, f"{category_details[x]().LOC_BASE}.description"),
				emoji = category_details[x]().ICON,
				value = x)
			for x in categories]

		class Selector(discord.ui.View):

			def __init__(self, ctx: discord.Interaction, base: discord.Embed, *, timeout: float = 180):
				super().__init__(timeout = timeout)
				self.origin = ctx
				self.embed = base

			@discord.ui.select(options = options, placeholder = get_local(lang, Help.LOC_BASE + '.placeholder'))
			async def callback(self, ctx: discord.Interaction, select: discord.ui.Select):
				from src.commands import sub_entries

				target = sub_entries[select.values[0]]
				self.embed.clear_fields()
				self.embed.description = None

				for i in target:
					entry = target[i]()
					syntax = get_local(lang, f"{entry.LOC_BASE}.syntax")
					short = get_local(lang, f"{entry.LOC_BASE}.short")

					self.embed.add_field(
						name = f"/{entry.COMMAND} {syntax}",
						value = f"{entry.ICON} {short}",
						inline = False )

				await self.origin.edit_original_response(content = get_local(lang, Help.LOC_BASE + '.selector_switch'), embed = self.embed)
				await ctx.response.send_message("Updated!", delete_after = 0)

			async def on_timeout(self) -> None:
				try:
					res = (await self.origin.original_response())
					await res.edit(content = f"⚠️ *{get_local(lang, 'system.timeout')}*\n{res.content}", view = None)
				except Exception as err:
					logs.error(err)
				return await super().on_timeout()

			async def on_error(self, ctx: discord.Interaction, error: Exception, item, /) -> None:
				await ctx.response(get_local(lang, 'system.error'))
				return await super().on_error(ctx, error, item)

		return Selector(ctx, base, timeout = timeout)

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

				# Retrieve User Language
				lang = database.fetch(-1, ctx.user.id).values[0]

				# Base Embed Structure
				embed = discord.embeds.Embed()
				embed.color = 0xb842ae
				embed.title = get_local(lang, Help.LOC_BASE + '.title')
				embed.set_footer(text = get_local(lang, Help.LOC_BASE + '.footer'), icon_url = "https://i.imgur.com/w1BwX4h.png")

				# Default Behavior
				if not command:

					for i in entries:
						if i in non_categorized:
							entry = entries[i]()
							syntax = get_local(lang, f"{entry.LOC_BASE}.syntax")
							short = get_local(lang, f"{entry.LOC_BASE}.short")

							embed.add_field(
								name = f"/{entry.COMMAND} {syntax}",
								value = f"{entry.ICON} {short}",
								inline = False )

					embed.add_field(
						name = "",
						value = get_local(lang, Help.LOC_BASE + '.selector_notice'),
						inline = False )

					from src.core.client import Client
					embed.description = get_local(lang, 'system.description')

					file_logo = discord.File("assets/logo.png", filename = "logo.png")
					embed.set_thumbnail(url="attachment://logo.png")
					await ctx.response.send_message(get_local(lang, Help.LOC_BASE + '.listed'), file = file_logo, embed = embed, ephemeral = True, view = Help.new_selector(ctx, embed, lang))

				# Search and Display Command
				else:

					if command in entries:
						entry: Any = entries[command]()
						syntax = get_local(lang, f"{entry.LOC_BASE}.syntax")
						description = construct.full_description(lang, entry.LOC_BASE)

						embed.description = f"{entry.ICON} __**/{entry.COMMAND} {syntax}:**__"
						if entry.ALIAS and len(entry.ALIAS) > 0:
							embed.description += "\n" + get_local(lang, 'command.base.aliases')
							for i in entry.ALIAS:
								embed.description += f" `{i}`"
						if description and len(description) > 0:
							embed.description += f"\n{description}"
						await ctx.response.send_message(get_local(lang, Help.LOC_BASE + '.found'), embed = embed, ephemeral = True)
					else:
						await ctx.response.send_message(get_local(lang, Help.LOC_BASE + '.notfound'), ephemeral = True)