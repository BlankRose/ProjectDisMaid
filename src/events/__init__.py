# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - __init__.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Sat Mar 11 22:22:04 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

from typing import Any
from src.utils.construct import import_entries

__all__: list[str]      = ["command_error", "on_message"]
entries: dict[str, Any] = import_entries(__all__, "src.events")