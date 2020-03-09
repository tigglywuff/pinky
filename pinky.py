import discord
import yaml

from discord import Message

pinky = discord.Client()


@pinky.event
async def on_ready():
    print('i\'m ready')


@pinky.event
async def on_message(message: Message):
    if message.author == pinky.user:
        return
    if message.content == 'ping':
        await message.channel.send(content='pong')

with open('config.yaml') as file:
    config = yaml.load(file)

pinky.run(config.get('token'))
