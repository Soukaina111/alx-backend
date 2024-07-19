#!/usr/bin/env python3
"""
This script provides a Server class that handles the pagination of a dataset
from a CSV file. The dataset is cached in memory to improve performance, and
the get_hyper_index method returns information about a specific page of data,
including the index of the next page.
"""

import csv
from typing import Dict, List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculates the start and end indices for a given page and page size.

    Args:
        page (int): The page number (starting from 1).
        page_size (int): The number of items to display per page.

    Returns:
        Tuple[int, int]: The start and end indices for the requested page.
    """
    start = (page - 1) * page_size
    end = start + page_size
    return start, end


class Server:
    """
    Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self._dataset = None

    def dataset(self) -> List[List]:
        """
        Retrieves the dataset from the CSV file, caching it in memory.

        Returns:
            List[List]: The dataset, with the header row removed.
        """
        if self._dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                self._dataset = [row for row in reader][1:]
        return self._dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Retrieves a page of data from the dataset.


        Returns:
            List[List]: The requested page of data.
        """
        assert page > 0 and page_size > 0
        start, end = index_range(page, page_size)
        data = self.dataset()
        return data[start:end]

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Retrieves information about a page of data, given the index of an item
        in the dataset and the desired page size.
        Returns:
            Dict: A dictionary containing the following keys:
                - index: The index of the requested item.
                - next_index: The index of the first item on the next page.
                - page_size: The number of items on the current page.
                - data: The data for the current page.
        """
        data = self.dataset()
        if index is None:
            index = 0
        assert 0 <= index < len(data)

        start, end = index_range(1, page_size)
        page_data = data[start:end]
        next_index = end

        for i, item in enumerate(data[end:], start=end):
            if len(page_data) < page_size:
                page_data.append(item)
            else:
                next_index = i
                break

        return {
            'index': index,
            'next_index': next_index,
            'page_size': len(page_data),
            'data': page_data,
        }
