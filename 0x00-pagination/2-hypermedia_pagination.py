#!/usr/bin/env python3
"""
Task 1: Simple pagination.
This module provides a simple implementation of a pagination system for a
CSV-based dataset of popular baby names.
"""

import csv
import math
from typing import List, Tuple, Dict


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Retrieves the index range from a given page and page size.

    This function takes two arguments:
    - `page`: the current page number (1-indexed)
    - `page_size`: the number of items to display per page

    Args:
        page (int): The current page number (1-indexed).
        page_size (int): The number of items to display per page.

    Returns:
        Tuple[int, int]: The start and end index of the current page.
    """
    # Calculate the start index of the current page
    start_index = (page - 1) * page_size

    # Calculate the end index of the current page
    end_index = start_index + page_size

    # Return the start and end index as a tuple
    return (start_index, end_index)


class Server:
    """
    Server class to paginate a database of popular baby names.

    This class provides a simple interface to fetch a page of data from a
    CSV-based dataset of popular baby names. The dataset is loaded and cached
    in memory upon the first request.

    Attributes:
        DATA_FILE (str): The filename of the CSV-based dataset.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        # Initialize the cached dataset to None
        self.__dataset = None

    def dataset(self) -> List[List]:
        """
        Cached dataset.
        This method returns the dataset of popular baby names loaded from the
        CSV file. The dataset is cached in memory after the first request to
        avoid reloading the data on subsequent requests.

        Returns:
            List[List]: The dataset of popular baby names, excluding the header
                row.
        """
        # If the dataset has not been loaded yet, load it from the CSV file
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                self.__dataset = [row for row in reader][1:]

        # Return the cached dataset
        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Retrieves a page of data.
        Args:
            page (int): The current page number (1-indexed). Defaults to 1.
            page_size (int): The number of items to display per page.
                Defaults to 10.
        Returns:
            List[List]: A list of lists representing the data rows for the
                current page.
        """
        # Ensure that the `page` and `page_size` parameters are valid integers
        assert type(page) == int and type(page_size) == int
        assert page > 0 and page_size > 0

        # Calculate the start and end index of the current page
        start, end = index_range(page, page_size)

        # Get the full dataset
        data = self.dataset()

        if start > len(data):
            return []

        # Return the rows of data for the current page
        return data[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """
        Retrieves information about a page.

        Args:
            page (int): The current page number (1-indexed). Defaults to 1.
            page_size (int): The number of items to display per page.
                Defaults to 10.

        Returns:
            Dict: A dictionary containing information about the current page.
        """
        # Get the data for the current page
        data = self.get_page(page, page_size)
        # Calculate the start and end index of the current page
        start, end = index_range(page, page_size)
        # Calculate the total number of pages
        total_pages = math.ceil(len(self.__dataset) / page_size)
        # Determine the next and previous page numbers (if they exist)
        next_page = page + 1 if end < len(self.__dataset) else None
        prev_page = page - 1 if start > 0 else None
        # Return a dictionary with the page information
        return {
            'page_size': len(data),
            'page': page,
            'data': data,
            'next_page': next_page,
            'prev_page': prev_page,
            'total_pages': total_pages
        }
