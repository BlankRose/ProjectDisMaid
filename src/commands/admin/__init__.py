# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - __init__.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Thu Mar  9 19:05:43 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.utils.construct import import_entries
class Admin():

	__all__ = ["mute", "unmute", "debug"]
	entries = import_entries(__all__, "src.commands.admin")

	icon = "🛠"
	title = "Server Administration"
	description = "Commands which handles all kind of moderations and systems"