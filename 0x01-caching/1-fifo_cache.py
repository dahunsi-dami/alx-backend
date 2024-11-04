#!/usr/bin/env python3
"""FIFO Cache class caching strategy implementation."""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """Defines a caching system with a FIFO eviction policy."""

    def __init__(self):
        """Initializes the cache."""
        super().__init__()
        self.order = []

    def put(self, key, item):
        """Adds an item in the cache."""
        if key is not None and item is not None:
            if key in self.cache_data:
                self.order.remove(key)

            self.order.append(key)
            self.cache_data[key] = item

            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                oldest_key = self.order.pop(0)
                del self.cache_data[oldest_key]
                print(f"DISCARD: {oldest_key}")

    def get(self, key):
        """Gets an item by key."""
        return self.cache_data.get(key, None)

