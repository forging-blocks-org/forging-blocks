"""Serialization infrastructure for the application.

Provides abstract and concrete codecs for encoding/decoding messages
to and from different representations.
"""

from ._dict_message_codec import DictMessageCodec
from ._message_codec import MessageCodec

__all__ = ["DictMessageCodec", "MessageCodec"]
