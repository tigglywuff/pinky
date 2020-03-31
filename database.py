import sqlite3

from discord import Guild
from discord import Member
from discord import Message
from discord import Role
from discord import TextChannel
from discord.utils import get
from typing import Union

conn = sqlite3.connect('pinky.db')
cursor = conn.cursor()


def initialize_guild(guild: Guild):
    """
    Creates row for this guild in guild_config
    """
    query = 'SELECT * FROM guild_config WHERE guild_id = {}'.format(guild.id)
    row = cursor.execute(query).fetchone()
    if row:
        return
    query = 'INSERT INTO guild_config (guild_id, guild_name) VALUES ({}, "{}")'.format(guild.id, guild.name)
    cursor.execute(query)
    conn.commit()


def get_admin_channel(guild: Guild) -> TextChannel:
    query = 'SELECT admin_channel FROM guild_config WHERE guild_id = {}'.format(guild.id)
    row = cursor.execute(query).fetchone()
    if row:
        channel = get(guild.channels, id=row[0])
        return channel
    return None


def update_admin_channel(guild: Guild, channel: TextChannel):
    query = 'UPDATE guild_config SET admin_channel = {} WHERE guild_id = {}'.format(channel.id, guild.id)
    cursor.execute(query)
    conn.commit()


def set_general_role(guild: Guild, role_name: str):
    role = get(guild.roles, name=role_name)
    query = 'UPDATE guild_config SET general_role = {} WHERE guild_id = {}'.format(role.id, guild.id)
    cursor.execute(query)
    conn.commit()


def get_general_role(guild: Guild) -> Role:
    query = 'SELECT general_role FROM guild_config WHERE guild_id = {}'.format(guild.id)
    row = cursor.execute(query).fetchone()
    if row:
        role = get(guild.roles, id=row[0])
        return role
    return None


def insert_welcome_message(message: Message, guild: Guild, user: Member):
    query = 'REPLACE INTO welcome_messages VALUES ({}, {}, {})'.format(message.id, guild.id, user.id)
    cursor.execute(query)
    conn.commit()


def delete_welcome_message(message: Message):
    query = 'DELETE FROM welcome_messages WHERE message_id = {}'.format(message.id)
    cursor.execute(query)
    conn.commit()


def is_welcome_message(message: Message) -> Union[int, bool]:
    query = 'SELECT user_id FROM welcome_messages WHERE message_id={} AND guild_id = {}'.format(message.id, message.guild.id)
    row = cursor.execute(query).fetchone()
    if row:
        return row[0]
    return False
