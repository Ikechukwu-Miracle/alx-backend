#!/usr/bin/python3
""" LFUCache Caching """
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """LFUCache Class """

    def __init__(self):
        """ Initialize LFUCache """
        self.access = []
        self.least_frequent = {}
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache """
        if key and item:
            if (len(self.access) >= self.MAX_ITEMS and
                    not self.cache_data.get(key)):
                delete = self.access.pop(0)
                self.least_frequent.pop(delete)
                self.cache_data.pop(delete)
                print('DISCARD: {}'.format(delete))

            if self.cache_data.get(key):
                self.access.remove(key)
                self.least_frequent[key] += 1
            else:
                self.least_frequent[key] = 0

            insert_index = 0
            while (insert_index < len(self.access) and
                   not self.least_frequent[self.access[insert_index]]):
                insert_index += 1
            self.access.insert(insert_index, key)
            self.cache_data[key] = item

    def get(self, key):
        """ Get item from key """
        if self.cache_data.get(key):
            self.least_frequent[key] += 1
            if self.access.index(key) + 1 != len(self.access):
                while (self.access.index(key) + 1 < len(self.access) and
                       self.least_frequent[key] >=
                       self.least_frequent[self.access[self.access.index(key) + 1]]):
                    self.access.insert(self.access.index(key) + 1,
                                      self.access.pop(self.access.index(key)))
        return self.cache_data.get(key)
        