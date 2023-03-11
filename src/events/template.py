# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - template.py                           #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Sat Mar 11 22:48:17 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

import discord

class T:

	"""
	Trigger template model
	"""

	#==-----==#

	@staticmethod
	def register(*, bot: discord.Client, **_: None):

		@bot.event
		async def event():
			pass