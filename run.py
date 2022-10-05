from src.core.construct import *
from datetime import datetime
from pathlib import Path
import logging as log

cwd 		= Path.cwd()
config_file	= "configs.json"
log_file	= datetime.now().strftime("Logs %d-%m-%Y %H-%M-%S.log")
log_level	= log.DEBUG

token = prepare(cwd, config_file, log_file, log_level)
run(token)