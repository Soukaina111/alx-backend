#!/usr/bin/env python3
"""
Task 3: Deletion-resilient hypermedia pagination
This module implements a server class to paginate a database of popular baby names.
"""

import csv
import math
from typing import Dict, List, Tuple


def calculate_index_range(current_page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculates the index range for a given page and page size.

    Args:
        current_page (int): The current page number.
        page_size (int): The desired number of items per page.

    Returns:
        Tuple[int, int]: The start and end indices for the current page.
    """
    start_index = (current_page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index


class PaginationServer:
    """
    Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__cached_dataset = None

    def get_dataset(self) -> List[List]:
        """
        Retrieves the cached dataset, or loads it from the CSV file if it's not cached.
        """
        if self.__cached_dataset is None:
            with open(self.DATA_FILE) as file:
                reader = csv.reader(file)
                self.__cached_dataset = [row for row in reader][1:]
        return self.__cached_dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Retrieves a page of data from the dataset.

        Args:
            page (int): The page number to retrieve.
            page_size (int): The desired number of items per page.

        Returns:
            List[List]: The data for the requested page.
        """
        assert isinstance(page, int) and isinstance(page_size, int)
        assert page > 0 and page_size > 0
        start_index, end_index = calculate_index_range(page, page_size)
        data = self.get_dataset()
        if start_index >= len(data):
            return []
        return data[start_index:end_index]

    def get_hypermedia_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Retrieves information about a page from a given index and with a specified size.

        Args:
            index (int, optional): The index to start from. If not provided, starts from 0.
            page_size (int): The desired number of items per page.

        Returns:
            Dict: A dictionary containing information about the page, including the index,
                  the next index, the page size, and the data for the page.
        """
        data = self.get_dataset()
        if index is not None:
            assert index >= 0 and index <= max(range(len(data)))
        page_data = []
        data_count = 0
        next_index = None
        start_index = index if index is not None else 0
        for i, item in enumerate(data):
            if i >= start_index and data_count < page_size:
                page_data.append(item)
                data_count += 1
                continue
            if data_count == page_size:
                next_index = i
                break
        data-pg = {
            'index': index,
            'next_index': next_index,
            'page_size': len(page_data),
            'data': page_data,
        }
        return data-pg
