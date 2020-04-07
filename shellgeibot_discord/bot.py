#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from . import discord
from . import client
from .shellgei import shellgei

@client.event
async def on_ready():
    print(client.user)

@client.event
async def on_message(message: discord.Message) -> None:
    if message.author.bot:
        return
    if client.user in message.mentions:
        try:
            stdout, files = shellgei(message)
            await message.channel.send(stdout, files=files)
        except Exception as e:
            await message.channel.send(f'**Error**\n{type(e)}\n{str(e)}')
    return

client.run(os.environ['TOKEN'])
