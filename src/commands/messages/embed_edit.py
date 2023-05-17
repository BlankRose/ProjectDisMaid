# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - embed_edit.py                         #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Wed May 17 16:19:56 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

import json
from src.utils import construct, predicates
import src.core.localizations as lz
import discord

class Embed_Edit:

	LOC_BASE = "command.messages.embed_edit"
	COMMAND = "embed_edit"
	ALIAS = []
	ICON = "📟"

	#==-----==#

	def count_fields(self, embed: discord.Embed) -> int:
		i = 0
		for _ in embed.fields:
			i += 1
		return i

	def count_character(self, embed: discord.Embed) -> int:
		i = 0
		if embed.title: i += len(embed.title)
		if embed.description: i += len(embed.description)
		if embed.footer.text: i += len(embed.footer.text)
		if embed.author.name: i += len(embed.author.name)
		for field in embed.fields:
			if field.name: i += len(field.name)
			if field.value: i += len(field.value)
		return i

	#==-----==#

	def register(self, cmd: discord.app_commands.CommandTree, entries: dict) -> None:

		sub_cmds = [
			"add_field", "add_footer", "add_author",
			"set_body", "set_field", "set_thumbnail", "set_title", "set_description", "set_color", "set_inline",
			"del_field", "del_title", "del_description", "del_footer", "del_author", "del_all_fields",
			"get_color", "get_raw"
		]

		async def autocomplete(ctx: discord.Interaction, current: str):
			return [
				discord.app_commands.Choice(name = entry, value = entry)
				for entry in sub_cmds if current.lower() in entry.lower()
			]

		registry = self.ALIAS + [self.COMMAND]
		short = self.ICON + " " + lz.get_local(lz.FALLBACK, f"{self.LOC_BASE}.short")
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = short)
			@discord.app_commands.describe(
				channel = "Channel where is located the embed",
				message_id = "Message which contains the embed",
				sub_command = "Sub command to run (check /help embed_edit)",
				title = "Title of new fields if applicable (Used for color in sub command set_color)",
				description = "Content of new fields if applicable (Used for color in sub command set_color)",
				image_url = "URL to the image to display if applicable",
				inline = "Wheter the new field shall be aligned on the same line",
				index = "Position of the targetted field or the new field")
			@discord.app_commands.autocomplete(sub_command = autocomplete)
			async def run(ctx: discord.Interaction, message_id: str, sub_command: str,
				channel: discord.TextChannel = None, title: str = None, description: str = None, image_url: str = None, inline: bool = False, index: int = None):

				lang = lz.get_userlang(ctx.user.id)

				# ############################## #
				#                                #
				#        VALIDITY CHECKER        #
				#                                #
				# ############################## #

				if not channel:
					channel = ctx.channel
				sub_command = sub_command.lower()

				if await predicates.from_guild(ctx, lang, False):
					if not await predicates.user_permissions(ctx, ctx.user, discord.Permissions(manage_messages = True), lang): return
					if not await predicates.app_permissions(ctx, discord.Permissions(send_messages = True), lang): return

				if not message_id.isdigit():
					return await ctx.response.send_message("The message ID doesn't actually looks like an ID.. It should be composed for digits!", ephemeral = True)

				try:
					target = await channel.fetch_message(int(message_id))
					if not target.author.id == ctx.application_id and not sub_command.startswith("get_"):
						return await ctx.response.send_message("I cannot edit embeds from others sources!", ephemeral = True)
				except:
					return await ctx.response.send_message("I couldnt fetch the given message! Are you sure its the right Channel and ID?..", ephemeral = True)
				if not sub_command in sub_cmds:
					return await ctx.response.send_message("The specified sub-command doesn't exists! Please look up `/help embed_edit` for further details", ephemeral = True)

				embed = target.embeds[0]
				if not embed:
					return await construct.reply(ctx, "The specified message doesn't contains any embed! You can create one with `/embed`.")

				total = self.count_fields(embed)
				len_current = self.count_character(embed)

				if title:
					title = title.replace('\\n', '\n')
				if description:
					description = description.replace('\\n', '\n')

				match sub_command:

				# ############################## #
				#                                #
				#       ADDITIONS COMMANDS       #
				#                                #
				# ############################## #

					case "add_field":
						if not title and not description:
							return await construct.reply(ctx, "You need to specify atleast a Title OR a Description!")
						if (title and len(title) > 256) or (description and len(description) > 1024):
							return await construct.reply(ctx, "You cannot exceed 256 characters for titles and 1024 for descriptions!")
						if total > 25:
							return await construct.reply(ctx, "You have reached the max capacity of fields this embed can hold (25 fields)!")
						if not index:		index = total + 1
						elif index <= 0:	index = 1
						elif index > total:	index = total + 1
						embed.insert_field_at(
							index = index - 1,
							name = title,
							value = description,
							inline = inline
						)

					case "add_footer":
						if not description:
							return await construct.reply(ctx, "You need to specify a Description!")
						if len(description) > 2048:
							return await construct.reply(ctx, "You cannot exceed 2048 characters for footers!")
						embed.set_footer(
							text = description,
							icon_url = image_url
						)

					case "add_author":
						if not description:
							return await construct.reply(ctx, "You need to specify a Description!")
						if len(description) > 256:
							return await construct.reply(ctx, "You cannot exceed 256 characters for authors!")
						embed.set_author(
							name = description,
							icon_url = image_url
						)

				# ############################## #
				#                                #
				#        SETTERS COMMANDS        #
				#                                #
				# ############################## #

					case "set_body":
						if not title and not description:
							return await construct.reply(ctx, "You need to specify atleast a Title OR a Description!")
						if (title and len(title) > 256) or (description and len(description) > 4096):
							return await construct.reply(ctx, "You cannot exceed 256 characters for titles and 4096 for descriptions!")
						embed.title = title
						embed.description = description

					case "set_field":
						if not title and not description:
							return await construct.reply(ctx, "You need to specify atleast a Title OR a Description!")
						if (title and len(title) > 256) or (description and len(description) > 1024):
							return await construct.reply(ctx, "You cannot exceed 256 characters for titles and 1024 for descriptions!")
						if not index:
							return await construct.reply(ctx, "Please specify an index!")
						if not (index > 0 and index <= total):
							return await construct.reply(ctx, "There is no fields at the specified index!")
						embed.set_field_at(
							index = index - 1,
							name = title,
							value = description,
							inline = inline
						)

					case "set_thumbnail":
						embed.set_thumbnail(url = image_url)

					case "set_title":
						if not title:
							return await construct.reply(ctx, "You need to specify the Title!")
						if len(title) > 256:
							return await construct.reply(ctx, "You cannot exceed 256 characters for titles!")
						if not index:
							embed.title = title
						elif not (index > 0 and index <= total):
							return await construct.reply(ctx, "There is no fields at the specified index!")
						else:
							embed.fields[index - 1].name = title

					case "set_description":
						if not description:
							return await construct.reply(ctx, "You need to specify the Title!")
						if not index:
							if len(description) > 4096:
								return await construct.reply(ctx, "You cannot exceed 4096 characters for descriptions!")
							embed.description = description
						else:
							if not (index > 0 and index <= total):
								return await construct.reply(ctx, "There is no fields at the specified index!")
							if len(description) > 1024:
								return await construct.reply(ctx, "You cannot exceed 1024 characters for descriptions!")
							embed.fields[index - 1].value = description

					case "set_color":
						color: int
						if title:
							color = construct.parse_hexa(title)
						elif description:
							color = construct.parse_hexa(description)
						else:
							return await construct.reply(ctx, "No color was given (Use either the title or description argument)!")
						if not color:
							return await construct.reply(ctx, "The given color is invalid!")
						embed.color = color

					case "set_inline":
						if not index:
							return await construct.reply(ctx, "Please specify an index!")
						if not (index > 0 and index <= total):
							return await construct.reply(ctx, "There is no fields at the specified index!")
						embed.set_field_at(
							index = index - 1,
							name = embed.fields[index - 1].name,
							value = embed.fields[index - 1].value,
							inline = inline
						)

				# ############################## #
				#                                #
				#      DESTRUCTIVE COMMANDS      #
				#                                #
				# ############################## #

					case "del_field":
						if not index:
							return await construct.reply(ctx, "Please specify an index!")
						if not (index > 0 and index <= total):
							return await construct.reply(ctx, "There is no fields at the specified index!")
						embed.remove_field(index - 1)

					case "del_title":
						if not index:
							if not embed.description:
								return await construct.reply(ctx, "There needs to be atleast a Title or Description!")
							embed.title = None
						else:
							if not (index > 0 and index <= total):
								return await construct.reply(ctx, "There is no fields at the specified index!")
							if not embed.fields[index - 1].value:
								return await construct.reply(ctx, "There needs to be atleast a Title or Description!")
							embed.fields[index - 1].name = None

					case "del_description":
						if not index:
							if not embed.title:
								return await construct.reply(ctx, "There needs to be atleast a Title or Description!")
							embed.description = None
						else:
							if not (index > 0 and index <= total):
								return await construct.reply(ctx, "There is no fields at the specified index!")
							if not embed.fields[index - 1].name:
								return await construct.reply(ctx, "There needs to be atleast a Title or Description!")
							embed.fields[index - 1].value = None

					case "del_footer":
						embed.remove_footer()

					case "del_author":
						embed.remove_author()

					case "del_all_fields":
						embed.clear_fields()

				# ############################## #
				#                                #
				#        GETTERS COMMANDS        #
				#                                #
				# ############################## #

					case "get_color":
						if not embed.color:
							return await construct.reply(ctx, "Target embed's color is not defined!")
						return await construct.reply(ctx, f"Target embed's color: 0x{hex(embed.color.value)[2:].upper()}")

					case "get_raw":
						reply: str = f"Here's the raw embed:\n```json\n{json.dumps(embed.to_dict(), indent = 2)}```"
						return await construct.reply(ctx, reply)

				# ############################## #
				#                                #
				#         UPDATE MESSAGE         #
				#                                #
				# ############################## #

				len_updated = self.count_character(embed)
				if len_updated > 6000:
					return await construct.reply(ctx, f"I couldn't update the embed as this reached the limits of 6000 characters!\nBefore: {len_current}\nAfter: {len_updated}")

				await target.edit(content = target.content, embed = embed)
				await construct.reply(ctx)