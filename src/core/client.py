import discord
import logging

class Client(discord.Client):
	"""
	Client class to handles discord.py API works
	
	Attributes:
	- `cmds`: CommandTree
	"""

	#==-----==#

	cmds = None

	#==-----==#

	def __init__(self, intents: discord.Intents = discord.Intents.default()):
		"""
		Initialize a new Client

		- `INTENTS` = Permission intents for the client
		"""
		super().__init__(intents=intents)
		self.synced = False

	#==-----==#

	async def on_ready(self):
		await self.wait_until_ready()
		if not self.synced:
			await self.cmds.sync()
			self.synced = True
		logging.info("The client is ready for usage!")

	async def on_disconnect(self) -> None:
		print("🎑\033[1;31m The maid has left the town.. \033[0m")
		logging.info("The client and the connection has been terminated!")

	async def on_connect(self) -> None:
		print("👒\033[1;32m The maid has came online! \033[0m")
		logging.info("The client and the connection has been etablished!")