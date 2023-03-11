# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - client.py                             #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Sat Mar 11 22:16:17 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.core import logs, configs
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

	DESCRIPTION = \
"""
Just a silly maid mouse for all of your needs~

This project was made to come with as many features as \
you could see on many bots while being fully free to use, \
without any paywalls or any voting requirements.

Support server:   [[Mystical Island](https://discord.gg/YDvpNYCcQf)]
Source (Github):  [[Project DisMaid](https://github.com/BlankRose/ProjectDisMaid)]
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
		print("🎑\033[1;31m The maid has left the town.. \033[0m")
		log.info("The connection has been terminated!")

	async def on_connect(self):
		print("👒\033[1;32m The maid has came online! \033[0m")
		log.info("The connection has been etablished!")

	#==-----==#

	async def close(self):
		print("🎑\033[1;31m The maid has left the town.. \033[0m")
		log.info("The connection has been terminated!")
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
	log.debug("Logs setup complete!..")
	log.debug(f"Running under python {sys.version}")

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

	entries = events.entries
	for i in events.entries:
		entries[i].register(cmd = cmds, bot = bot)

	try:
		bot.cmds = cmds
		bot.run(token)
	except Exception as err:
		log.error(f"The bot couldnt be started! Internet issues or Invalid Token?\nError: {err}")
