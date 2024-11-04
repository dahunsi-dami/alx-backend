#!/usr/bin/env python3
"""MRU Cache class caching implementation strategy."""

from base_caching import BaseCaching
from collections import OrderedDict


class MRUCache(BaseCaching):
    """Defines a caching system with an MRU eviction policy."""
    def __init__(self):
        """Initializes the cache and usage tracking."""
        super().__init__()
        self.cache_data = OrderedDict()
        self.usedKeys = []

    def put(self, key, item):
        """Adds an item to the cache with MRU eviction policy."""
        if key is not None and item is not None:
            self.cache_data[key] = item
            
            if key not in self.usedKeys:
                self.usedKeys.append(key)
            else:
                self.usedKeys.append(self.usedKeys.pop(self.usedKeys.index(key)))
            
            if len(self.usedKeys) > BaseCaching.MAX_ITEMS:
                discard_key = self.usedKeys.pop(-2)
                del self.cache_data[discard_key]
                print(f"DISCARD: {discard_key}")

    def get(self, key):
        """Gets an item by key, marking it as most recently used."""
        if key is not None and key in self.cache_data:
            self.usedKeys.append(self.usedKeys.pop(self.usedKeys.index(key)))
            return self.cache_data[key]
        return None

