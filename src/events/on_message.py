# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - on_message.py                         #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Sun May 21 21:49:27 CEST 2023     #
#      ||  '-'                                                          #
# ********************************************************************* #

import discord
import logging as log

import src.core.database as db
from math import ceil

	#==-----==#

class On_Message:

	"""
	Triggers when a message is sent in any available
	servers, and does specific tasks regarding what
	was sent.
	"""

	@staticmethod
	def register(*, bot: discord.Client, **_: None):

		if not bot.intents.message_content:
			return log.info("Event on_message requierds the following intent: message_content!")

		@bot.event
		async def on_message(msg: discord.Message):

			if not msg.guild: return
			if msg.author.bot: return
			if msg.is_system(): return

			info = db.fetch(msg.guild.id, msg.author.id)
			if not info: return

			info['xp'] += calc_xp(len(msg.content))
			lvl_up = calc_lvl(info['level'] + 1)

			if info['xp'] > lvl_up:
				info['level'] += 1
				info['xp'] -= lvl_up
			db.store(msg.guild.id, msg.author.id, info)

	#==-----==#

LVL_BASE = 100
MINIMUM_LENGTH = 10
XP_CAP = 15

def calc_xp(x: int) -> int:
	if x < MINIMUM_LENGTH: return 0
	return min(ceil(((x - MINIMUM_LENGTH) / (6 + x / 5)) ** 1.5 * 1.35), XP_CAP)

def calc_lvl(x: int) -> int:
	return ceil(LVL_BASE * x * (x ** -.3))
