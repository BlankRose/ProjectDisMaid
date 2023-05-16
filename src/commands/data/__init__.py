# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - __init__.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Tue May 16 18:50:39 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.utils.construct import import_entries
class Data:

	__all__ = ["level"]
	entries = import_entries(__all__, "src.commands.data")

	LOC_BASE = "categories.data"
	ICON = "🔖"