# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - __init__.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Thu Mar  9 19:06:59 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.utils.construct import import_entries
class Scripts:

	__all__ = ["hello", "random"]
	entries = import_entries(__all__, "src.commands.scripts")

	icon = "🎲"
	title = "Utilities & Entertainment"
	description = "Commands mostly here to diversify a bit the server"