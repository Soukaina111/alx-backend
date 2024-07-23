#!/usr/bin/python3
"""LRU Cache Replacement Implementation Class"""

# Import the RLock class from the 'threading' module
from threading import RLock

# Import the BaseCaching class from the 'base_caching' module
BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """
    An implementation of LRU (Least Recently Used) Cache

    Attributes:
        __keys (list): Stores cache keys from least to most accessed
        __rlock (RLock): Lock accessed resources to prevent race condition
    """
    def __init__(self):
        """
        Instantiation method, sets instance attributes.
        """
        super().__init__()
        self.__keys = []
        self.__rlock = RLock()

    def put(self, key, item):
        """
        Add an item to the cache.

        Args:
            key (Any): The key associated with the item.
            item (Any): The item to be added to the cache.
        """
        # Check if the key and item are not None
        if key is not None and item is not None:
            # Call the _balance method to handle cache eviction if needed
            keyO = self._balance(key)
            # Acquire the lock to ensure thread-safe access to the cache
            with self.__rlock:
                # Update the cache_data dictionary with the new key-value pair
                self.cache_data.update({key: item})
            # If a key was evicted, print the DISCARD message
            if keyO is not None:
                print('DISCARD: {}'.format(keyO))

    def get(self, key):
        """
        Retrieve an item from the cache by its key.

        Args:
            key (Any): The key of the item to be retrieved.
        """
        # Acquire the lock to ensure thread-safe access to the cache
        with self.__rlock:
            value = self.cache_data.get(key, None)
            if key in self.__keys:
                self._balance(key)
        return value

    def _balance(self, keyIn):
        """
        Removes the least recently used item from the cache at MAX size.

        Args:
            keyIn (Any): The key of the new item to be added to the cache.

        Returns:
            The key of the evicted item, or None if no eviction was necessary.
        """
        keyO = None
        with self.__rlock:
            # Get the current length of the __keys list
            LengthK = len(self.__keys)
            if keyIn not in self.__keys:
                if len(self.cache_data) == BaseCaching.MAX_ITEMS:
                    keyO = self.__keys.pop(0)
                    self.cache_data.pop(keyO)
            else:
                self.__keys.remove(keyIn)
            self.__keys.insert(LengthK, keyIn)
        return keyO
