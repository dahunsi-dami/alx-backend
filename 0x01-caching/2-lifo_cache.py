#!/usr/bin/env python3
"""LIFO Cache class caching implementation strategy."""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """Defines a caching system with a LIFO eviction policy."""
    def __init__(self):
        """Initializes the cache."""
        super().__init__()
        self.keys_order = []

    def put(self, key, item):
        """Adds an item in the cache."""
        if key is not None and item is not None:
            if key in self.cache_data:
                self.cache_data[key] = item
            else:
                self.cache_data[key] = item
                self.keys_order.append(key)

            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                last_key = self.keys_order.pop(-2)
                del self.cache_data[last_key]
                print(f"DISCARD: {last_key}")

    def get(self, key):
        """Gets an item by key."""
        return self.cache_data.get(key, None)
