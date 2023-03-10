# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - __init__.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Fri Mar 10 18:56:14 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

from typing import Any
from src.utils.construct import import_entries

#-- TYPE HINTS --#

_entry_t                    = dict[str, Any]
_sub_t                      = dict[str | None, _entry_t]

#-- DEFINITIONS --#

root: str                   = "src.commands"
categories: list[str]       = ["admin", "messages", "scripts"]
non_categorized: list[str]  = ["help"]

category_details: _entry_t  = import_entries(categories, root)
entries: _entry_t           = import_entries(non_categorized, root)

sub_entries: _sub_t         = {**{None: entries}, **{k: category_details[k]().entries for k in categories}}
entries: _entry_t           = {k: v for i in categories for d in (sub_entries[i], entries) for k, v in d.items()}