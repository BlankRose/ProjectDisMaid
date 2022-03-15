from ressources import log_handler as logx
from datetime import datetime
from pathlib import Path
import logging as log
import asyncio
import discord
import json
import os

###		INITIALIZE
###	Fetch and sets up configs

cwd = Path.cwd()

launch_time = datetime.now()
logs_folder = Path.joinpath(cwd, "logs")
logs_file = Path.joinpath(logs_folder, launch_time.strftime("Logs %d-%m-%Y %H-%M-%S.logs"))

if not Path.exists(logs_folder):
	logs_folder.mkdir()

log.basicConfig(filename=logs_file,
				filemode="w",
				level=log.DEBUG,
				format="[%(asctime)s] %(levelname)s >> %(message)s")

configs = "configs.json"
log.info(f"Fetching data from {configs}..")
with open(cwd.joinpath(configs), "r") as file:
	try:
		data = json.load(file)
	except:
		logx.danger("Couldn't fetch any data! ABORTING!")
log.info("Successfully gathered data")

essentials = (("token", str),)
for i in essentials:
	try:
		if not isinstance(data[i[0]], i[1]):
			raise TypeError
	except TypeError:
		logx.danger(f"Expected an {i[1]} for IMPORTANT config: {i[0]}! ABORTING!")
	except:
		logx.danger(f"Missing IMPORTANT config: {i[0]}! ABORTING!")

options = (("maxLogs", int, 5),)
for i in options:
	try:
		if not isinstance(data[i[0]], i[1]):
			raise TypeError
	except TypeError:
		log.warning(f"Expected an {i[1]} for option config {i[0]}. Initializing to default: {i[2]}")
		data[i[0]] = i[2]
	except:
		log.warning(f"Missing option config: {i[0]}. Initializing to default: {i[2]}")
		data[i[0]] = i[2]

log.debug(f"Successfully loaded data: {data}")

logs = []
for f in os.listdir(logs_folder):
	f = logs_folder.joinpath(f)
	if (os.path.isfile(f)):
		logs.append(f)
logs.sort(key=lambda t:-os.stat(t).st_mtime)
if data["maxLogs"] >= 0:
	log.debug("Searching for excess of logs and cleaning..")
	for excess in logs[data["maxLogs"] + 1:]:
		os.remove(excess)
	log.debug("Cleaning done!")

###		DISCORD API
###	Get ready and runs the bot online

bot = discord.Client()

async def main():
	try:
		await bot.login(token=data["token"], bot=True)
	except discord.LoginFailure:
		logx.danger(f"Provided token in {configs} is invalid! ABORTING!")
	except:
		logx.danger(f"Couldn't connect to servers!")
	await bot.wait_until_ready()
	await bot.connect(reconnect=True)

asyncio.run(main())