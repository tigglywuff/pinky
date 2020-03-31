import database
import discord

from discord import Reaction
from discord.utils import get


REACTION = {
    'promote': '⏫',
    'boot': '🥾',
}

async def handle_reaction(reaction: Reaction):
    user_id = database.is_welcome_message(reaction.message)
    if not user_id:
        return

    guild = reaction.message.guild
    user = get(guild.members, id=user_id)
    if reaction.emoji == REACTION['promote']:
        await user.add_roles(database.get_general_role(guild))
    elif reaction.emoji == REACTION['boot']:    
        await user.kick()
    await reaction.message.delete()
    database.delete_welcome_message(reaction.message)
