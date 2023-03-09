# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - try.py                                #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Thu Mar  9 14:49:27 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

from src.utils.construct import import_entries

categories = ['a', 'b']
entries = {'main': 56, 'alt': 456}
sub_entries = import_entries(categories, "test")

print(entries)
print(sub_entries['a'].entries)
print(sub_entries['b'].entries)