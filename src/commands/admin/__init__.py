# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - __init__.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Tue May 16 18:52:45 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.utils.construct import import_entries
class Admin():

	__all__ = ["mute", "unmute", "debug"]
	entries = import_entries(__all__, "src.commands.admin")

	LOC_BASE = "categories.admin"
	ICON = "🛠"