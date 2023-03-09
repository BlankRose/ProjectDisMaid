# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - __init__.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Thu Mar  9 18:13:50 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.utils.construct import import_entries

root = "src.commands"
categories: list = ["admin", "messages", "scripts"]
non_categorized: list = ["help"]

category_details = import_entries(categories, root)
entries = import_entries(non_categorized, root)

sub_entries = {**{None: entries}, **{k: category_details[k]().entries for k in categories}}
entries = {k: v for i in categories for d in (sub_entries[i], entries) for k, v in d.items()}