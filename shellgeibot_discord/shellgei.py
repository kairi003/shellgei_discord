#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import re
import base64
import json
import itertools
import requests
from . import client
from . import discord
from . import utils
from . import b64int
from .exceptions import *

class MessageFormats:
    _PATTERN_MENTION = re.compile(rf'_@([{b64int.CHARS}=]+)_')

    def __init__(self, message: discord.Message):
        self._message = message
        self.display_dict = {format_: display for (format_, display) in self._display_dict_generator()}
        self.pattern = re.compile('|'.join(map(lambda key: re.escape(key), self.display_dict.keys())))
        used_formats = sorted(map(lambda m:m[0], re.finditer(self.pattern, message.content)), key=lambda f: len(self.display_dict[f]))
        self.used_formats_len = len(used_formats)
        self._format_dict = {}
        self._formats = [None] * self.used_formats_len
        self._repls = [None] * self.used_formats_len
        for i, format_ in enumerate(used_formats):
            self._format_dict[format_] = i
            display_len = utils.get_east_asian_width_count(self.display_dict[format_])
            b64_index = b64int.dec_to_b64(i)
            repl_len = len(b64_index) + 3
            self._formats[i] = format_ + ' ' * max(repl_len - display_len, 0)
            self._repls[i] = f"_@{b64_index + '=' * max(display_len - repl_len, 0)}_"
    
    def _display_dict_generator(self):
        message = self._message
        for channel in message.channel_mentions:
            yield f'<#{channel.id}>', channel.name
        for member in message.mentions:
            yield re.escape(f'<@{member.id}>'), member.display_name
            yield re.escape(f'<@!{member.id}>'), member.display_name
        if message.guild is not None:
            for role in message.role_mentions:
                yield re.escape(f'<@&{role.id}>'), role.name
            for emoji in message.guild.emojis:
                yield re.escape(f'<:{emoji.name}:{emoji.id}>'), '___'
                yield re.escape(f'<a:{emoji.name}:{emoji.id}>'), '___'
    
    def get_repl(self, match: re.Match):
        if match[0] in self.display_dict:
            index = self._format_dict[match[0]]
            return self._repls[index]
        else:
            return match[0]
    
    def get_mention(self, match: re.Match):
        b64_index = match.group(1).replace('=', '')
        index = b64int.b64_to_dec(b64_index)
        if index < self.used_formats_len:
            return self._formats[index]
        else:
            return match[0]        
    
    def content_repl(self, content):
        return re.sub(self.pattern, self.get_repl, content)
        
    def content_mention(self, content):
        return re.sub(self._PATTERN_MENTION, self.get_mention, content)



def shellgei(message):
    content = message.content
    content = re.sub(rf'<@!?{client.user.id}>', r'', content)
    if m := re.search(r'```(\S*)([\s\S]*?)```', content):
        if re.fullmatch(r'\s*', m[2]):
            content = m[1]
        else:
            content = m[2]

    formats = MessageFormats(message)
    content = formats.content_repl(content)

    b64_images = [base64.b64encode(res.content) for att in message.attachments if (res := requests.get(att.url)).ok]
    res = requests.post('https://websh.jiro4989.com/api/shellgei', json.dumps({'code': content, 'images': b64_images}), timeout=(9, 30))
    res.raise_for_status()
    res_json = json.loads(res.content)

    if res_json['status'] != 0:
        raise APIError(res_json['system_message'])

    stdout = formats.content_mention(res_json['stdout']) if res_json['stdout'] else None
    files = [discord.File(io.BytesIO(b_img), filename=f'{i}.{utils.imghdr.what(None, b_img)}')
            for i, img in enumerate(res_json['images'])
            if (b_img := base64.b64decode(img['image']))]
    
    if not stdout and not files and res_json['stderr']:
        raise ShellExecuteError(res_json['stderr'])
    
    return (stdout, files)
