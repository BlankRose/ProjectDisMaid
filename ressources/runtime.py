from ressources import commands
from ressources.configs import Config
import discord
import logging

class Client(discord.Client):

	async def on_disconnect(self):
		print("🎑\033[1;31m The maid has left the town.. \033[0m")
		logging.info("The client and the connection has been terminated!")
	async def on_connect(self):
		print("👒\033[1;32m The maid has came online! \033[0m")
		logging.info("The client and the connection has been etablished!")
	
	async def on_message(self, msg: discord.message.Message):
		if msg.author == self.user:
			return
		if msg.content.startswith(Config.data["cmdPrefix"]):
			logging.info(f"Executing command: {msg.content} ({msg.author})")
			try:
				cmd = msg.content[len(Config.data["cmdPrefix"]):].split(" ")
				entry = commands.entries[cmd[0]]()
				await entry.run(commands.entries, msg)
				logging.info("Successfully executed the command!")
			except KeyError:
				logging.info("User tried to execute an unknown command!")
			except Exception as errMsg:
				logging.warning(f"An error occured while trying to execute command: {errMsg}")