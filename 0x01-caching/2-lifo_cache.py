#!/usr/bin/env python3
"""
Defines a LIFOCache class that inherits from BaseCaching.
"""

BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """
    Implements a caching system using LIFO algorithm.
    """

    def __init__(self):
        """
        Initializes the LIFO cache.
        """
        super().__init__()

    def put(self, key, item):
        """
        Adds an item to the cache.
        """
        if key is None or item is None:
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # Find the last item put in cache (LIFO algorithm)
            last_key = list(self.cache_data.keys())[-1]
            del self.cache_data[last_key]
            print("DISCARD:", last_key)

        self.cache_data[key] = item

    def get(self, key):
        """
        Retrieves an item from the cache.
        """
        if key is None or key not in self.cache_data:
            return None

        return self.cache_data[key]
