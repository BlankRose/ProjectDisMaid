from typing import List
import discord
from src.core import construct, predicates

class Embed_edit():

	command = "embed_edit"
	alias = []

	syntax = command + " <Message ID> <Sub Command> ..."
	icon = "📟"

	short = icon + " Edits an already existing embed"
	description = \
"""
Edits an already existing embed (can be created with the command \
`embed`) and grants even more controls and flexibility over its \
design with its various sub-commands.

__ARGUMENTS:__
`Channel` - *Channel where is located the embed to edit*
`Message ID` - *Message which contains the embed to edit*
`Sub Commands` - *Commands to executes, which can be:*

`add_field` - *Adds a normal field, at given index*
ARGS: <Title AND/OR Description> [Inline] [Index]
`add_footer` - *Adds a footer field (replaces)*
ARGS: <Description> [Image URL]
`add_author` - *Adds an author field (replaces)*
ARGS: <Description> [Image URL]
`set_body` - *Changes the content of the main field*
ARGS: <Title AND/OR Description>
`set_field` - *Changes the content of any fields*
ARGS: <Title AND/OR Description> [Inline] [Index]
`set_thumbnail` - *Changes the thumbnail*
ARGS: [Image URL]
`del_field` - *Deletes a field, at given index*
ARGS: <Index>
`del_footer` - *Removes the footer field*
`del_author` - *Removes the author field*
`del_all_fields` - *Deletes every single fields*

__SUB ARGUMENTS:__
`Title` - *Text of the field's header*
`Description` - *Content of the field's body*
`Image URL` - *URL to the image to display OR removes it in thumbnail context*
`Inline` - *Wether fields should be aligned on same line or not*
`Index` - *Position of the field (from 1 to Number of Fields)*

__UNSPECIFIED VALUES:__
`Title` `Description` - *Won't add anything new to the embed BUT one must be specified!*
`Image URL` *Won't display any images*
`Inline` - *Will be defined as False*
`Index` - *Will be considered the very last index*

__SIDE NOTES:__
Due to discord's limitations, embeds has their set limits as such:
 - `Titles` are limited to **256** characters
 - `Descriptions` are limited to **4096** characters
 - `Embeds` can only contains up to **25** fields
 - `Fields titles` are limited to **256** characters
 - `Fields descriptions` are limited to **1024** characters
 - `Footers` are limited to **2048** characters
 - `Author name` is limited to **256** characters
 - Finally, the total amount of characters cannot exceed **6000**
Extra arguments not used by the sub commands will be ignored.

__REQUIERED PERMISSIONS:__
Application: `Send Messages`
Caller: `Manage Messages`
"""

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
			"set_body", "set_field", "set_thumbnail",
			"del_field", "del_footer", "del_author", "del_all_fields"
		]

		async def autocomplete(interaction: discord.Interaction, current: str) -> List[discord.app_commands.Choice[str]]:
			return [
				discord.app_commands.Choice(name = entry, value = entry)
				for entry in sub_cmds if current.lower() in entry.lower()
			]

		registry = self.alias + [self.command]
		for i in registry:

	#==-----==#

			@cmd.command(name = i, description = self.short)
			@discord.app_commands.describe(
				channel = "Channel where is located the embed",
				message_id = "Message which contains the embed",
				sub_command = "Sub command to run (check /help embed_edit)",
				title = "Title of new fields if applicable",
				description = "Content of new fields if applicable",
				image_url = "URL to the image to display if applicable",
				inline = "Wheter the new field shall be aligned on the same line",
				index = "Position of the targetted field or the new field")
			@discord.app_commands.autocomplete(sub_command = autocomplete)
			async def run(interaction: discord.Interaction, channel: discord.TextChannel, message_id: str, sub_command: str,
				title: str = None, description: str = None, image_url: str = None, inline: bool = False, index: int = 0):

				# Conditions
				if await predicates.from_guild(interaction, False):
					if not await predicates.user_permissions(interaction, interaction.user, discord.Permissions(manage_messages = True)): return
					if not await predicates.app_permissions(interaction, discord.Permissions(send_messages = True)): return
				if not message_id.isdigit():
					return await interaction.response.send_message("The message ID doesn't actually looks like an ID.. It should be composed for digits!", ephemeral = True)

				# Error Management
				try:
					target = await channel.fetch_message(int(message_id))
					if not target.author.id == interaction.application_id:
						return await interaction.response.send_message("I cannot edit embeds from others sources!", ephemeral = True)
				except:
					return await interaction.response.send_message("I couldnt fetch the given message! Are you sure its the right Channel and ID?..", ephemeral = True)

				if not sub_command in sub_cmds:
					return await interaction.response.send_message("The specified sub-command doesn't exists! Please look up `/help embed_edit` for further details", ephemeral = True)

				embed = target.embeds[0]
				if not embed:
					return await construct.reply(interaction, "The specified message doesn't contains any embed! You can create one with `/embed`.")

				total = self.count_fields(embed)
				len_current = self.count_character(embed)

				# Add Field
				if sub_command == "add_field":
					if not title and not description:
						return await construct.reply(interaction, "You need to specify atleast a Title OR a Description!")
					if (title and len(title) > 256) or (description and len(description) > 1024):
						return await construct.reply(interaction, "You cannot exceed 256 characters for titles and 1024 for descriptions!")
					if total > 25:
						return await construct.reply(interaction, "You have reached the max capacity of fields this embed can hold (25 fields)!")
					if index <= 0 or index > total:
						index = total
					embed.insert_field_at(
						index = index - 1,
						name = title,
						value = description,
						inline = inline
					)

				# Add Footer
				if sub_command == "add_footer":
					if not description:
						return await construct.reply(interaction, "You need to specify a Description!")
					if len(description) > 2048:
						return await construct.reply(interaction, "You cannot exceed 2048 characters for footers!")
					embed.set_footer(
						text = description,
						icon_url = image_url
					)

				# Add Author
				if sub_command == "add_author":
					if not description:
						return await construct.reply(interaction, "You need to specify a Description!")
					if len(description) > 256:
						return await construct.reply(interaction, "You cannot exceed 256 characters for authors!")
					embed.set_author(
						name = description,
						icon_url = image_url
					)

				# Set Body
				if sub_command == "set_body":
					if not title and not description:
						return await construct.reply(interaction, "You need to specify atleast a Title OR a Description!")
					if (title and len(title) > 256) or (description and len(description) > 4096):
						return await construct.reply(interaction, "You cannot exceed 256 characters for titles and 4096 for descriptions!")
					embed.title = title
					embed.description = description

				# Set Field
				if sub_command == "set_field":
					if not title and not description:
						return await construct.reply(interaction, "You need to specify atleast a Title OR a Description!")
					if (title and len(title) > 256) or (description and len(description) > 1024):
						return await construct.reply(interaction, "You cannot exceed 256 characters for titles and 1024 for descriptions!")
					if index > 0 and index <= total:
						return await construct.reply(interaction, "There is no fields at the specified index!")
					embed.set_field_at(
						index = index - 1,
						name = title,
						value = description,
						inline = inline
					)

				# Set Thumbnail
				if sub_command == "set_thumbnail":
					embed.set_thumbnail(url = image_url)

				# Delete Field
				if sub_command == "del_field":
					if index > 0 and index <= total:
						return await construct.reply(interaction, "There is no fields at the specified index!")
					embed.remove_field(index - 1)

				# Delete Footer
				if sub_command == "del_footer":
					embed.remove_footer()

				# Delete Author
				if sub_command == "del_author":
					embed.remove_author()

				# Delete Every Fields
				if sub_command == "del_all_fields":
					embed.clear_fields()

				# Final checks and Send everything
				len_updated = self.count_character(embed)
				if len_updated > 6000:
					return await construct.reply(interaction, f"I couldn't update the embed as this reached the limits of 6000 characters!\nBefore: {len_current}\nAfter: {len_updated}")

				await target.edit(content = target.content, embed = embed)
				await construct.reply(interaction)