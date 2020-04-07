#!/usr/bin/env python
# -*- coding: utf-8 -*-

CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXWGabcdefghijklmnopqrstuvwxyz0123456789+/'
RCHARS = {c: i for i, c in enumerate(CHARS)}

def dec_to_b64(num: int) -> str:
    q, r = divmod(num, 64)
    if q:
        return dec_to_b64(q) + CHARS[r]
    return CHARS[r]

def b64_to_dec(b64: str) -> int:
    num = 0
    for i in range(len(b64)):
        num += RCHARS[b64[-(i + 1)]] * 64**i
    return num