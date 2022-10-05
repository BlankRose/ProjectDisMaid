import traceback
from src import commands
from src.core import *
from pathlib import Path
import logging as log
import discord.app_commands as app
import discord

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

def setup(cmds: app.CommandTree) -> None:
	@cmds.command(name="hai", description="💬 Say hello to the maid")
	async def hello(interaction: discord.Interaction):
		import random as rng
		caseA = ["Hai sweetheart~",
				"Hello there~",
				"Hoi!"]
		strA = caseA[rng.randrange(0, len(caseA))]
		caseB = ["(^owo^)s *Meow.*",
				"How are you?",
				"Would you like some cookies?",
				"Have you seen my cat? I can't find it anywhere."]
		strB = caseB[rng.randrange(0, len(caseB))]
		await interaction.response.send_message(f"{strA}\n{strB}", ephemeral=True)

def run(token: str) -> None:
	bot = client.Client()
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

	client.Client.cmds = cmds
	bot.run(token)