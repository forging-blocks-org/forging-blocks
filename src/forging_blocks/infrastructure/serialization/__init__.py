"""Serialization infrastructure for the application.

Provides protocols and utilities for serializing and deserializing
domain objects to and from plain dictionaries.
"""

from .serializable import Serializable

__all__ = ["Serializable"]
