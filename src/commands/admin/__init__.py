# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - __init__.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Fri Mar 10 20:54:17 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.utils.construct import import_entries
class Admin():

	__all__ = ["mute", "unmute", "debug"]
	entries = import_entries(__all__, "src.commands.admin")

	ICON = "🛠"
	TITLE = "Server Administration"
	DESCRIPTION = "Commands which handles all kind of moderations and systems"