# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - command_error.py                      #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Sat Mar 11 22:31:24 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

import discord
import discord.app_commands as app

import logging as log
import traceback

class Command_Error:

	"""
	Triggers when commands throws an error instead
	of quitting the programm to allow the bot running
	even in the most pathetic cases of error, which
	was not handled correctly.
	"""

	#==-----==#

	@staticmethod
	def register(*, cmd: app.CommandTree, **_: None):

		@cmd.error
		async def event(ctx: discord.Interaction, error: app.AppCommandError):
			if isinstance(error, app.CommandOnCooldown):
				await ctx.response.send_message(f"Please, lemme relax a bit between tasks..\nI'll be avaible again for that in {error.retry_after}!")
			else:
				print("\033[1;31;2mWARNING: \033[0;1;31mAn error occured!\n\n", traceback.format_exc())
				log.error(traceback.format_exc())