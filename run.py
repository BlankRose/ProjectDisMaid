from ressources import *
from datetime import datetime
from pathlib import Path
import logging as log

cwd = Path.cwd()
config_file = "configs.json"
launch_time = datetime.now()
launch_time_str = launch_time.strftime("Logs %d-%m-%Y %H-%M-%S.log")

info = logs.Logs(folder=cwd.joinpath("logs"),
				 file=launch_time_str)
log.basicConfig(filename=info.file,
				filemode="w",
				level=log.DEBUG,
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
					options=(("maxLogs", int, 5), ("cmdPrefix", str, "!")))):
	logs.Logs.danger("ABORTING..")

info.clean(config.data["maxLogs"])

bot = runtime.Client()
bot.run(data["token"])