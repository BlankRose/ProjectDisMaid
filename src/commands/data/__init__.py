# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - __init__.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Sat Mar 11 20:47:12 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.utils.construct import import_entries
class Data:

	__all__ = ["level"]
	entries = import_entries(__all__, "src.commands.data")

	ICON = "🔖"
	TITLE = "Roles & Levels"
	DESCRIPTION = "Commands about any kind of enrolling (Comming Soon..)"