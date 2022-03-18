from ressources.commands import *
from ressources.configs import Config
import discord

class Help():

	short = "The maid's guidelines"
	description = """This command will open the maid's guidelines, where is located the `command` when specified or gives the summary if nothing is given.\n
					ARGUMENTS :
					`[COMMAND]` - *Search for a specefic command*"""
	syntax = "help [command]"
	icon = ":book:"

	async def run(self, entries: dict, msg: discord.message.Message):
		cmd = msg.content[len(Config.data["cmdPrefix"]):].split(" ")
		embed = discord.embeds.Embed()
		embed.color = 0xb842ae
		embed.title = "**Maids' Guidelines**"

		if len(cmd) < 2:
			embed.description = "*Comming soon.. TM*"
			embed.set_thumbnail(url="https://i.imgur.com/4NKOPyu.png")
			for i in entries:
				entry = entries[i]()
				embed.add_field(
					name=entry.icon + " " + Config.data["cmdPrefix"] + entry.syntax,
					value=entry.short,
					inline=False
				)

		else:
			for i in entries:
				if i == cmd[1]:
					entry = entries[i]()
					embed.description = entry.icon + " __**" + entry.syntax + ":**__\n" + entry.description
					break
			else:
				await msg.reply("Sorry, I didn't found any entry in the guidelines.")
				return

		embed.set_footer(text="Edited by Rosie#4721", icon_url="https://i.imgur.com/w1BwX4h.png")
		await msg.reply(content="Here is what I found:", embed=embed)