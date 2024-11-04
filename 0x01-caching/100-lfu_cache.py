#!/usr/bin/env python3
"""LFU Cache class caching implementation strategy."""

from base_caching import BaseCaching
from collections import defaultdict, OrderedDict


class LFUCache(BaseCaching):
    """Defines a caching system with an LFU eviction policy."""

    def __init__(self):
        """Initializes the cache and frequency tracking."""
        super().__init__()
        self.cache_data = {}
        self.freq_map = defaultdict(OrderedDict)
        self.key_freq = {}

    def put(self, key, item):
        """Adds an item to the cache with LFU eviction policy."""
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.update_frequency(key)
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            min_freq = min(self.freq_map.keys())
            lfu_key, _ = self.freq_map[min_freq].popitem(last=False)

            del self.cache_data[lfu_key]
            del self.key_freq[lfu_key]
            print(f"DISCARD: {lfu_key}")

            if not self.freq_map[min_freq]:
                del self.freq_map[min_freq]

        self.cache_data[key] = item
        self.key_freq[key] = 1
        self.freq_map[1][key] = item

    def get(self, key):
        """Gets an item by key, marking it as recently used."""
        if key is None or key not in self.cache_data:
            return None

        self.update_frequency(key)
        return self.cache_data[key]

    def update_frequency(self, key):
        """Updates the frequency of a given key."""
        current_freq = self.key_freq[key]
        new_freq = current_freq + 1

        del self.freq_map[current_freq][key]

        if not self.freq_map[current_freq]:
            del self.freq_map[current_freq]

        self.key_freq[key] = new_freq
        self.freq_map[new_freq][key] = self.cache_data[key]
