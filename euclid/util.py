# coding: utf-8


def to_bytes(s):
    if isinstance(s, bytes):
        return s
    return s.encode('u8')


def to_str(b):
    if isinstance(b, str):
        return b
    return b.decode('u8')
