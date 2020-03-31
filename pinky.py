import database
import discord
import yaml

from discord import Embed
from discord import Member
from discord import Message
from discord.utils import get

from message_handler import handle_message
from reaction_handler import handle_reaction
from reaction_handler import REACTION

pinky = discord.Client()


@pinky.event
async def on_ready():
    print('Currently connected to guilds:')
    for guild in pinky.guilds:
        print(' - {}'.format(guild.name))
        database.initialize_guild(guild)
    print('I\'m ready!')


@pinky.event
async def on_member_join(member: Member):
    admin_channel = database.get_admin_channel(member.guild)
    embed = Embed(title='New member joined', description=member.name).set_thumbnail(url=member.avatar_url)
    sent_message = await admin_channel.send(embed=embed)
    await sent_message.add_reaction(REACTION['promote'])
    await sent_message.add_reaction(REACTION['boot'])
    database.insert_welcome_message(sent_message, member.guild, member)


@pinky.event
async def on_reaction_add(reaction, user):
    if (user == pinky.user):
        return
    await handle_reaction(reaction)


@pinky.event
async def on_message(message: Message):
    if message.author == pinky.user:
        return
    if not pinky.user in message.mentions:
        return
    await handle_message(message)

with open('config.yaml') as file:
    config = yaml.load(file)

pinky.run(config.get('token'))
