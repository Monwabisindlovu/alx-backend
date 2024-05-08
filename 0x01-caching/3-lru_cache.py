#!/usr/bin/env python3
"""
Defines a LRUCache class that inherits from BaseCaching.
"""

BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """
    Implements a caching system using LRU algorithm.
    """

    def __init__(self):
        """
        Initializes the LRU cache.
        """
        super().__init__()
        self.lru_keys = []

    def put(self, key, item):
        """
        Adds an item to the cache.
        """
        if key is None or item is None:
            return

        # If the key already exists, move it to the end (most recently used)
        if key in self.cache_data:
            self.lru_keys.remove(key)
        # If cache is full, remove the least recently used item
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            lru_key = self.lru_keys.pop(0)
            del self.cache_data[lru_key]
            print("DISCARD:", lru_key)

        self.cache_data[key] = item
        self.lru_keys.append(key)

    def get(self, key):
        """
        Retrieves an item from the cache.
        """
        if key is None or key not in self.cache_data:
            return None

        # Move the key to the end (most recently used)
        self.lru_keys.remove(key)
        self.lru_keys.append(key)

        return self.cache_data[key]
