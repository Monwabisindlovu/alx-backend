#!/usr/bin/env python3
"""
Defines a FIFOCache class that inherits from BaseCaching.
"""

BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """
    Implements a caching system using FIFO algorithm.
    """

    def __init__(self):
        """
        Initializes the FIFO cache.
        """
        super().__init__()

    def put(self, key, item):
        """
        Adds an item to the cache.
        """
        if key is None or item is None:
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # Find the first item put in cache (FIFO algorithm)
            first_key = next(iter(self.cache_data))
            del self.cache_data[first_key]
            print("DISCARD:", first_key)

        self.cache_data[key] = item

    def get(self, key):
        """
        Retrieves an item from the cache.
        """
        if key is None or key not in self.cache_data:
            return None

        return self.cache_data[key]
