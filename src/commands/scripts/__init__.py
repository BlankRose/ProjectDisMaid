# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - __init__.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Fri Mar 10 20:54:08 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.utils.construct import import_entries
class Scripts:

	__all__ = ["hello", "random"]
	entries = import_entries(__all__, "src.commands.scripts")

	ICON = "🎲"
	TITLE = "Utilities & Entertainment"
	DESCRIPTION = "Commands mostly here to diversify a bit the server"