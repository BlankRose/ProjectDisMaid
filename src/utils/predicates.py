# ********************************************************************* #
#          .-.                                                          #
#    __   /   \   __                                                    #
#   (  `'.\   /.'`  )   DisMaid - predicates.py                         #
#    '-._.(;;;)._.-'                                                    #
#    .-'  ,`"`,  '-.                                                    #
#   (__.-'/   \'-.__)   BY: Rosie (https://github.com/BlankRose)        #
#       //\   /         Last Updated: Sat Mar 11 22:55:59 CET 2023      #
#      ||  '-'                                                          #
# ********************************************************************* #

import logging
import discord

from src.utils.construct import reply

async def from_guild(ctx: discord.Interaction, msg: bool = True) -> bool:
	"""
	Checks wether the interaction is made in a guild
	"""
	if not ctx.guild:
		if msg: await reply(ctx, "You must be in a guild to execute this command!")
		return False
	return True

	#==-----==#

async def from_dm(ctx: discord.Interaction, msg: bool = True) -> bool:
	"""
	Checks wether the interaction is made in DMs
	"""
	if ctx.guild:
		if msg: await reply(ctx, "You must be in DMs to execute this command!")
		return False
	return True

	#==-----==#

async def is_member(ctx: discord.Interaction, user: discord.User, msg: bool = True) -> bool:
	"""
	Checks wether the user is in the guild
	"""
	if not user:
		logging.warning("Trying to predicate if member on non-existant user! BLOCKED")
		return False
	if not await from_guild(ctx, False):
		logging.warning("Trying to predicate if member out of guilds! IGNORED")
		return True
	if not ctx.guild.get_member(user.id):
		if msg: await reply(ctx, "The given user cannot be found! Are you sure he's part of this guild?..")
		return False
	return True

	#==-----==#

async def member_permissions(ctx: discord.Interaction, user: discord.Member, perms: discord.Permissions, msg: bool = True) -> bool:
	"""
	Checks if the member has the sufficient permissions (Shall be used in guilds!)
	"""
	if not user:
		logging.warning("Trying to predicate permissions on non-existant member! BLOCKED")
		return False

	async def e() -> bool:
		if msg: await reply(ctx, "You don't has the sufficient permissions to execute this command!")
		return False

	cmp = user.guild_permissions
	if cmp.is_superset(perms): return True
	return await e()

	if cmp.administrator: return True
	if perms.administrator: return await e()
	if perms.add_reactions and not cmp.add_reactions: return await e()
	if perms.attach_files and not cmp.attach_files: return await e()
	if perms.ban_members and not cmp.ban_members: return await e()
	if perms.change_nickname and not cmp.change_nickname: return await e()
	if perms.connect and not cmp.connect: return await e()
	if perms.create_instant_invite and not cmp.create_instant_invite: return await e()
	if perms.create_private_threads and not cmp.create_private_threads: return await e()
	if perms.create_public_threads and not cmp.create_public_threads: return await e()
	if perms.deafen_members and not cmp.deafen_members: return await e()
	if perms.embed_links and not cmp.embed_links: return await e()
	if perms.external_emojis and not cmp.external_emojis: return await e()
	if perms.external_stickers and not cmp.external_stickers: return await e()
	if perms.kick_members and not cmp.kick_members: return await e()
	if perms.manage_channels and not cmp.manage_channels: return await e()
	if perms.manage_emojis and not cmp.manage_emojis: return await e()
	if perms.manage_events and not cmp.manage_events: return await e()
	if perms.manage_guild and not cmp.manage_guild: return await e()
	if perms.manage_messages and not cmp.manage_messages: return await e()
	if perms.manage_nicknames and not cmp.manage_nicknames: return await e()
	if perms.manage_permissions and not cmp.manage_permissions: return await e()
	if perms.manage_roles and not cmp.manage_roles: return await e()
	if perms.manage_threads and not cmp.manage_threads: return await e()
	if perms.manage_webhooks and not cmp.manage_webhooks: return await e()
	if perms.mention_everyone and not cmp.mention_everyone: return await e()
	if perms.moderate_members and not cmp.moderate_members: return await e()
	if perms.move_members and not cmp.move_members: return await e()
	if perms.mute_members and not cmp.mute_members: return await e()
	if perms.priority_speaker and not cmp.priority_speaker: return await e()
	if perms.read_message_history and not cmp.read_message_history: return await e()
	if perms.read_messages and not cmp.read_messages: return await e()
	if perms.request_to_speak and not cmp.request_to_speak: return await e()
	if perms.send_messages and not cmp.send_messages: return await e()
	if perms.send_messages_in_threads and not cmp.send_messages_in_threads: return await e()
	if perms.send_tts_messages and not cmp.send_tts_messages: return await e()
	if perms.speak and not cmp.speak: return await e()
	if perms.stream and not cmp.stream: return await e()
	if perms.use_application_commands and not cmp.use_application_commands: return await e()
	if perms.use_embedded_activities and not cmp.use_embedded_activities: return await e()
	if perms.use_voice_activation and not cmp.use_voice_activation: return await e()
	if perms.view_audit_log and not cmp.view_audit_log: return await e()
	if perms.view_guild_insights and not cmp.view_guild_insights: return await e()
	return True

	#==-----==#

async def user_permissions(ctx: discord.Interaction, user: discord.User, perms: discord.Permissions, msg: bool = True) -> bool:
	"""
	Checks if the user has the sufficient permissions (Shall be used in guilds!)
	"""
	if not user:
		logging.warning("Trying to predicate permissions on non-existant user! BLOCKED")
		return False
	if not await from_guild(ctx, False):
		logging.warning("Trying to predicate permissions out of guilds! IGNORED")
		return True
	return await member_permissions(ctx, ctx.guild.get_member(user.id), perms, msg)

	#==-----==#

async def app_permissions(ctx: discord.Interaction, perms: discord.Permissions, msg: bool = True) -> bool:
	"""
	Checks if the application has the sufficient permissions (Shall be used in guilds!)
	"""
	if not await from_guild(ctx, False):
		logging.warning("Trying to predicate permissions out of guilds! IGNORED")
		return True
	if not await member_permissions(ctx, ctx.guild.get_member(ctx.client.user.id), perms, False):
		if msg: await reply(ctx, "I don't has the sufficient permissions to perform this task!")
		return False
	return True