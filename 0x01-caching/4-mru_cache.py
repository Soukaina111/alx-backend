#!/usr/bin/python3
"""MRU Cache Replacement Implementation Class
"""
# Importing RLock from threading module for thread-safe operations
from threading import RLock

# Dynamically importing BaseCaching class
BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """
    An implementation of MRU(Most Recently Used) Cache

    Attributes:
        __keys (list): Stores cache keys from least to most accessed
        __rlock (RLock): Lock accessed resources to prevent race condition
    """

    def __init__(self):
        """ Instantiation method, sets instance attributes
        """
        super().__init__()
        self.__keys = []
        self.__rlock = RLock()

    def put(self, key, item):
        """ Add an item in the cache

        Args:
            key: The unique identifier for the item to be cached.
            item: The actual content to be cached.

        """
        if key is not None and item is not None:
            # Check and possibly remove the least recently used item
            OutK = self._balance(key)
            with self.__rlock:  # Ensure thread safety
                # Update the cache with the new item
                self.cache_data.update({key: item})
            if OutK is not None:
                # Inform about discarded item if necessary
                print('DISCARD: {}'.format(OutK))

    def get(self, key):
        """ Get an item by key

        Args:
            key: The unique identifier for the item to retrieve from the cache.

        Returns:
        Updates the access order of the retrieved item.
        """
        with self.__rlock:  # Ensure thread safety
            # Retrieve the item from the cache
            value = self.cache_data.get(key, None)
            if key in self.__keys:
                # Update the access order of the retrieved item
                self._balance(key)
        return value

    def _balance(self, keyIn):
        """ Removes the earliest item from the cache at MAX size

        Args:
            keyIn: The key of the item whose access order needs to be updated.

        Returns:
            The key of the discarded item, if any, otherwise None.

        Also updates the access order of the specified key.
        """
        OutK = None
        with self.__rlock:  # Ensure thread safety
            # Current number of keys in the cache
            keysLength = len(self.__keys)
            if keyIn not in self.__keys:
                if len(self.cache_data) == BaseCaching.MAX_ITEMS:
                    # Remove the least recently used item
                    OutK = self.__keys.pop(keysLength - 1)
                    self.cache_data.pop(OutK)  # Remove the item from the cache
            else:
                self.__keys.remove(keyIn)
            self.__keys.insert(keysLength, keyIn)
        return OutK
