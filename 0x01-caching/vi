#!/usr/bin/env python3
"""Defines a MRUCache class that inherits from BaseCaching."""


BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """Implements a caching system using MRU algorithm."""

    def __init__(self):
        """Initializes the MRU cache."""
        super().__init__()

    def put(self, key, item):
        """Adds an item to the cache."""
        if key is None or item is None:
            return

        # If the key already exists, move it to the end (most recently used)
        if key in self.cache_data:
            del self.cache_data[key]

        # If cache is full, remove the most recently used item
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            mru_key = max(self.cache_data, key=self.cache_data.get)
            del self.cache_data[mru_key]
            print("DISCARD:", mru_key)

        self.cache_data[key] = item

    def get(self, key):
        """Retrieves an item from the cache."""
        if key is None or key not in self.cache_data:
            return None

        # Move the key to the end (most recently used)
        value = self.cache_data.pop(key)
        self.cache_data[key] = value

        return value
