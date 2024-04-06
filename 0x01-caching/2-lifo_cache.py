#!/usr/bin/env python3
"""LIFOCache module"""
BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """LIFOCache that inherits from BaseCaching"""

    def __init__(self):
        """Constructor"""
        super().__init__()

    def put(self, key, item):
        """Add an item in the cache"""
        if key is not None and item is not None:
            if key in self.cache_data:
                del self.cache_data[key]
            if len(self.cache_data) >= self.MAX_ITEMS:
                discardedKey = list(self.cache_data.keys())[-1]
                del self.cache_data[discardedKey]
                print("DISCARD:", discardedKey)
            self.cache_data[key] = item

    def get(self, key):
        """Get an item by key"""
        if key in self.cache_data:
            return self.cache_data[key]
        return None
