# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - __init__.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Mon Mar  6 16:38:43 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

__all__ = ["hello", "random", "mute", "unmute", "embed", "embed_edit", "embed_clone"]

from src.commands import help
import importlib
import sys

entries = {}
__all__.append("help")
for i in __all__:
	name = "src.commands." + i
	importlib.import_module(name)
	entries[i] = getattr(sys.modules[name], i.capitalize())
