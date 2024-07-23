#!/usr/bin/python3
"""MRU Cache Replacement Implementation Class
"""
from threading import RLock

BaseCaching = import('base_caching').BaseCaching


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
    self.__keys = []  # Initialize the list to store cache keys
    self.__rlock = RLock()  # Create a reentrant lock for thread safety


def put(self, key, item):
    """ Add an item in the cache
    """
    if key is not None and item is not None:
        # Call the _balance method to update the cache
        keyO = self._balance(key)
        with self.__rlock:
            # Add the new item to the cache
            self.cache_data.update({key: item})
        if keyO is not None:
            # Print the discarded key, if any
            print('DISCARD: {}'.format(keyO))


def get(self, key):
    """ Get an item by key
    """
    with self.__rlock:
        # Retrieve the item from the cache
        value = self.cache_data.get(key, None)
        if key in self.__keys:
            self._balance(key)  # Call the _balance method to update the cache
    return value


def _balance(self, keyIn):
    """ Removes the earliest item from the cache at MAX size
    """
    keyO = None  # Initialize the variable to store the discarded key
    with self.__rlock:
        LenghtOFK = len(self.__keys)  # Get the length of the __keys list
        if keyIn not in self.__keys:
            if len(self.cache_data) == BaseCaching.MAX_ITEMS:
                # Remove the least recently used key
                keyO = self.__keys.pop(LenghtOFK - 1)
                # Remove the corresponding item from the cache
                self.cache_data.pop(keyO)
        else:
            self.__keys.remove(keyIn)  # Remove the existing key from the list
        # Add the key to the end of the list
        self.__keys.insert(LenghtOFK, keyIn)
    return keyO
