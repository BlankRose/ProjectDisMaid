# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - __init__.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Tue May 16 18:50:44 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.utils.construct import import_entries
class Messages:

	__all__ = ["embed", "embed_edit", "embed_clone"]
	entries = import_entries(__all__, "src.commands.messages")

	LOC_BASE = "categories.messages"
	ICON = "📯"