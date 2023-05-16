# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - __init__.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Tue May 16 18:53:26 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.utils.construct import import_entries
class Scripts:

	__all__ = ["hello", "random"]
	entries = import_entries(__all__, "src.commands.scripts")

	LOC_BASE = "categories.scripts"
	ICON = "🎲"