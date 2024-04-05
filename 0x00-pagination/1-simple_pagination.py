#!/usr/bin/env python3
"""Class for pagination"""
import csv
from typing import List, Tuple


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Returns lists from dataset containing rows"""
        assert type(page) is int and page > 0
        assert type(page_size) is int and page_size > 0

        start_index, end_index = index_range(page, page_size)
        
        return self.dataset()[start_index:end_index]


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Returns a tuple of size two containing a start index and an end index
    """
    start_index = (page - 1) * page_size
    end_index = page * page_size

    return (start_index, end_index)
