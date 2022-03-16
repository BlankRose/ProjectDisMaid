import discord
import logging
import configs

config = configs.Config.data

class Client(discord.Client):

	async def on_connect(self):
		print("👒\033[1;32m The maid has came online! \033[0m")
		logging.info("The client and the connection has been etablished!")
	
	async def on_message(self, msg):
		if msg.author == self.user or not msg.content.startswith(config["cmdPrefix"]):
			return