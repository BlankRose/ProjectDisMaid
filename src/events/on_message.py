# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - on_message.py                         #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Sat Mar 11 23:25:39 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

import discord
import logging as log

class On_Message:

	"""
	Triggers when a message is sent in any available
	servers, and does specific tasks regarding what
	was sent.
	"""

	#==-----==#

	@staticmethod
	def register(*, bot: discord.Client, **_: None):

		if not bot.intents.message_content:
			return log.info("Event on_message requierds the following intent: message_content!")

		@bot.event
		async def on_message(msg: discord.Message):

			if not msg.guild: return
			if msg.author.bot: return

			# LEVELING SYSTEM HERE...