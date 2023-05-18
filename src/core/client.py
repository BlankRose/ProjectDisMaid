# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - client.py                             #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Thu May 18 14:10:14 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

import src.core.localizations as lz
from src.core import logs, configs, database
from src import commands, events
from pathlib import Path
import sys

import discord.app_commands as app
import logging as log
import discord

class Client(discord.Client):

	"""
	Client class to handles discord.py API workflow

	Attributes
	----------
	cmds: `CommandTree`
		Command tree of the running instance
	"""

	#==-----==#

	def __init__(self):
		intents = discord.Intents.default()
		intents.members = True
		intents.message_content = True

		super().__init__(
			intents=intents,
			activity=discord.Activity(name = "/help for commands", type = discord.ActivityType.watching))

		self.cmds: app.CommandTree = None
		self.synced = False

	#==-----==#

	async def on_ready(self):
		await self.wait_until_ready()
		if not self.synced:
			await self.cmds.sync()
			self.synced = True
		log.info("The client is ready for usage!")

	async def on_disconnect(self):
		print("👒\033[1;33m The maid has took a break.. \033[0m")
		log.info("The connection has been lost! Retrying..")

	async def on_connect(self):
		print("🌍\033[1;32m The maid has came online! \033[0m")
		log.info("The connection has been etablished!")

	#==-----==#

	async def close(self):
		print("\033[2K🌙\033[1;31m The maid has left the town.. \033[0m")
		log.info("The connection has been terminated!")
		database.save()
		await super().close()

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
	log.info("Logs setup complete!..")
	log.info(f"Running under python {sys.version}")

	config = configs.Config()
	config.fetch(cwd, config_file)
	data = config.data
	configs.Config.data = config.data
	if not (config.check(
			verify=data,
			important=(
				("token", str),
				("localizations", str),
				("database", str)),
			options=(
				("maxLogs", int, 5),
				("autoSave", bool, True),
				("autoSave-time", int, 600))
		)):
		logs.Logs.danger("ABORTING..")

	database.load()
	lz.load_locals(data["localizations"])

	info.clean(data["maxLogs"])
	return (data["token"])

	#==-----==#

def run(token: str) -> None:
	bot = Client()
	cmds = app.CommandTree(bot)

	entries = commands.entries
	for i in entries:
		entries[i]().register(cmds, entries)

	entries = events.entries
	for i in events.entries:
		entries[i].register(cmd = cmds, bot = bot)

	try:
		bot.cmds = cmds
		bot.run(token, log_handler = None)
	except Exception as err:
		log.error(f"The bot couldnt be started! Internet issues or Invalid Token?\nError: {err}")
