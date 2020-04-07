#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unicodedata
import imghdr

imghdr.tests.append(lambda h, f: 'jpeg' if h[:2] == b'\xff\xd8' else None)


def get_east_asian_width_count(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1
    return count