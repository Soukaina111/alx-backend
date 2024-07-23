#!/usr/bin/python3
"""Basic Cache implementation Class"""

# Import the BaseCaching class from the 'base_caching' module
BaseCaching = __import__('base_caching').BaseCaching

class BasicCache(BaseCaching):
    """
    A basic cache implementation class

    Attributes:
        MAX_ITEMS: number of items that can be stored in the cache
    """

    def put(self, key, item):
        """
        Add an item to the cache.

        Args:
            key (Any): The key associated with the item.
            item (Any): The item to be added to the cache.
        """
        if key is not None and item is not None:
            self.cache_data.update({key: item})

    def get(self, key):
        """
        Retrieve an item from the cache by its key.

        Args:
            key (Any): The key of the item to be retrieved.

        Returns:
            The value associated with the given key, or None if the key is not found.
        """
        return self.cache_data.get(key, None)
