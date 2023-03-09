# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - __init__.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Thu Mar  9 19:05:25 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.utils.construct import import_entries
class Messages:

	__all__ = ["embed", "embed_edit", "embed_clone"]
	entries = import_entries(__all__, "src.commands.messages")

	icon = "📯"
	title = "System Messages"
	description = "Commands that revolves around system messages"