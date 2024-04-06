#!/usr/bin/env python3
"""MRUCache module"""
BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """MRUCache that inherits from BaseCaching"""

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.access = []

    def put(self, key, item):
        """Add an item in the cache"""
        if key is not None and item is not None:
            if key in self.cache_data:
                self.access.remove(key)
            elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discardedKey = self.access.pop()
                del self.cache_data[discardedKey]
                print("DISCARD:", discardedKey)
            self.cache_data[key] = item
            self.access.append(key)

    def get(self, key):
        """Get an item by key"""
        if key is not None and key in self.cache_data:
            self.access.remove(key)
            self.access.append(key)
            return self.cache_data[key]
        return None
