#!/usr/bin/env python3
"""Modules that contains the BasicCache class."""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
    BasicCache defines a basic caching system-
    -without any limit.
    """
    def put(self, key, item):
        """Adds an item in the cache."""
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """Gets an item w/ the key."""
        return self.cache_data.get(key, None)
