import database

from discord import Message
from typing import Callable


NO_ENTRY = '⛔'
OK = '✅'

async def handle_message(message: Message):
    message_string = message.clean_content.lower().replace('@pinky', '').strip()

    # Check for params after a ':'
    args = message_string.split(':')
    func = get_matching_function(args[0].strip())
    if (func):
        if len(args) > 1:
            await func(message, *args[1:])
        else:
            await func(message)


async def get_admin_channel(message: Message):
    admin_channel = database.get_admin_channel(message.guild)
    if admin_channel:
        await message.channel.send(content=admin_channel.name)
    else:
        await message.channel.send(content='it hasn\'t been set')


async def set_admin_channel(message: Message):
    # Only the guild owner can set this
    if (message.author == message.guild.owner):
        database.update_admin_channel(message.guild, message.channel)
        await message.add_reaction(OK)
    else:
        await message.add_reaction(NO_ENTRY)


async def set_general_role(message: Message, *args):
    # This can only be set in the admin channel
    admin_channel = database.get_admin_channel(message.guild)
    if message.channel == admin_channel:
        database.set_general_role(message.guild, args[0].strip())
        await message.add_reaction(OK)
    else:
        await message.add_reaction(NO_ENTRY)


async def hello(message: Message):
    await message.channel.send(content='Hello')
    

def get_matching_function(name: str) -> Callable:
    name = name.replace(' ', '_')
    if name == 'get_matching_function':
        False
    if name in globals().keys():
        return globals()[name]
    return False


async def promote_everyone(message: Message):
    admin_channel = database.get_admin_channel(message.guild)
    if (message.author == message.guild.owner):
        for user in message.guild.members:
            await user.add_roles(database.get_general_role(message.guild))
        await message.add_reaction(OK)
    else:
        await message.add_reaction(NO_ENTRY)
