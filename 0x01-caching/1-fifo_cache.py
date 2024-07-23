#!/usr/bin/python3
""" Caching :FIFO Cache Replacement Implementation Class"""

# Import the RLock class from the 'threading' module
from threading import RLock

# Import the BaseCaching class from the 'base_caching' module
BaseCaching = __import__('base_caching').BaseCaching

class FIFOCache(BaseCaching):
    """
    An implementation of FIFO (First In First Out) Cache

    Attributes:
        __keys (list): Stores cache keys in order of entry using `.append`
        __rlock (RLock): Lock accessed resources to prevent race condition
    """
    def __init__(self):
        """
        Instantiation method, sets instance attributes.
        """
        super().__init__()
        self.__keys = []  # Initialize the list to store cache keys in order
        self.__rlock = RLock()  # Initialize the reentrant lock

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
            OutK = self._balance(key)
            # Acquire the lock to ensure thread-safe access to the cache
            with self.__rlock:
                # Update the cache_data dictionary with the new key-value pair
                self.cache_data.update({key: item})
            # If a key was evicted, print the DISCARD message
            if OutK is not None:
                print('DISCARD: {}'.format(OutK))

    def get(self, key):
        """
        Retrieve an item from the cache by its key.

        Args:
            key (Any): The key of the item to be retrieved.

        Returns:
            The value associated with the given key, or None if the key is not found.
        """
        # Acquire the lock to ensure thread-safe access to the cache
        with self.__rlock:
            # Retrieve the value associated with the given key from the cache_data dictionary
            return self.cache_data.get(key, None)

    def _balance(self, keyIn):
        """
        Removes the oldest item from the cache at MAX size.

        Args:
            keyIn (Any): The key of the new item to be added to the cache.

        Returns:
            The key of the evicted item, or None if no eviction was necessary.
        """
        OutK = None
        # Acquire the lock to ensure thread-safe access to the cache
        with self.__rlock:
            # Check if the new key is not already in the cache
            if keyIn not in self.__keys:
                # Get the current length of the __keys list
                LengthofK = len(self.__keys)
                # If the cache is at maximum capacity, evict the oldest item
                if len(self.cache_data) == BaseCaching.MAX_ITEMS:
                    OutK = self.__keys.pop(0)  # Remove the oldest key
                    self.cache_data.pop(OutK)  # Remove the corresponding item from the cache
                # Add the new key to the end of the __keys list
                self.__keys.insert(LengthofK, keyIn)
        return OutK
