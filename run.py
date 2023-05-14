# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - run.py                                #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Sat Mar 11 21:36:20 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

import sys

if sys.version_info[0] < 3:		exit(print(f"Python >= 3.10 requierd!\nCurrently using: {sys.version}"))
if sys.version_info[1] < 10:	exit(print(f"Python >= 3.10 requierd!\nCurrently using: {sys.version}"))

import logging as log
from datetime import datetime
from pathlib import Path

from src.core import client

cwd 		= Path.cwd()
config_file	= "configs.json"
log_file	= datetime.now().strftime("Logs %d-%m-%Y %H-%M-%S.log")
log_level	= log.DEBUG

token = client.prepare(cwd, config_file, log_file, log_level)
client.run(token)