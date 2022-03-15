import logging as log
from pathlib import Path
from datetime import datetime
import asyncio
import discord

###
### SCRIPTS SETUP
### Loads settings
###

launch_time = datetime.now()
logs_folder = Path.joinpath(Path.cwd(), "logs")
logs_file = Path.joinpath(logs_folder, launch_time.strftime("Logs %d-%m-%Y %H-%M.logs"))

if not Path.exists(logs_folder):
	logs_folder.mkdir()

log.basicConfig(filename=logs_file,
				filemode="w",
				level=log.DEBUG,
				format="[%(asctime)s] %(levelname)s >> %(message)s")
log.info(f"Starting script..")

###
### DISCORD API
### Get ready and starts the bot
###

bot = discord.Client()

async def main():
	await bot.login(token="ODIwNjY3MDY4ODE0MDY1Njk0.YE4fxA.7_zpO6aJP-Tch051S4168gDFoJY", bot=True)
	await bot.wait_until_ready()
	await bot.connect(reconnect=True)

asyncio.run(main())