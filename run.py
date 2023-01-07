# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - run.py                                #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Fri Jan  6 14:43:13 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.core.client import *
from datetime import datetime
from pathlib import Path
import logging as log

cwd 		= Path.cwd()
config_file	= "configs.json"
log_file	= datetime.now().strftime("Logs %d-%m-%Y %H-%M-%S.log")
log_level	= log.DEBUG

token = prepare(cwd, config_file, log_file, log_level)
run(token)