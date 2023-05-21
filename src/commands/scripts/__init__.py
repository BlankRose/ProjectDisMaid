# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - __init__.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Sun May 21 19:54:17 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.utils.construct import import_entries
class Scripts:

	__all__ = ["hello", "random", "chess"]
	entries = import_entries(__all__, "src.commands.scripts")

	LOC_BASE = "categories.scripts"
	ICON = "🎲"