#!/usr/bin/env python3
"""
Pagination helper function.

This module provides a utility function to
calculate the index range for a given
page and page size in a paginated dataset.
"""
from typing import Tuple


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
