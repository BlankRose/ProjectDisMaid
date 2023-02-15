from src.core import logs, configs
import discord.app_commands as app
from src import commands
from pathlib import Path
import logging as log
import traceback
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
		intents.members = True
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

	#==-----==#

def prepare(cwd: Path, config_file: str, log_file: str, log_level: int = log.DEBUG) -> str:

	info = logs.Logs(folder=cwd.joinpath("logs"),
					 file=log_file)
	log.basicConfig(filename=info.file,
					filemode="w",
					level=log_level,
					format="[%(asctime)s] %(levelname)s >> %(message)s")
	logs.Logs.folder = info.folder
	logs.Logs.file = info.file
	log.debug("Logs setup complete!..")

	config = configs.Config()
	config.fetch(cwd, config_file)
	data = config.data
	configs.Config.data = config.data
	if not (config.check(verify=data,
						important=(("token", str),),
						options=(("maxLogs", int, 5),))):
		logs.Logs.danger("ABORTING..")
	
	info.clean(data["maxLogs"])
	return (data["token"])

	#==-----==#

def run(token: str) -> None:
	bot = Client()
	cmds = app.CommandTree(bot)

	entries = commands.entries
	for i in entries:
		entries[i]().register(cmds, entries)

	@cmds.error
	async def cmd_error(interaction: discord.Interaction, error: app.AppCommandError):
		if isinstance(error, app.CommandOnCooldown):
			await interaction.response.send_message(f"Please, lemme relax a bit between tasks..\nI'll be avaible again for that in {error.retry_after}!")
		else:
			log.error(traceback.format_exc())

	Client.cmds = cmds
	try:
		bot.run(token)
	except:
		log.error("The bot couldnt be started! Internet issues or Invalid Token?")
