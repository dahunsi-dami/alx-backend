#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict, Union


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Deletion-resilient paginated data returning function.

        Args:
            index: starting index for pagination. None by default.
            page_size: number of iterms per page. 10 by default.

        Returns:
            dict: dictionary containing:
                - index: current start index of the page.
                - data: list of dataset rows for current page.
                - page_size: actual size of returned dataset page.
                - next_index: next index to query w/ or NOne if no more data.

        Raises:
            AssertionError: if index isn't valid int/out of range or
                            page_size isn't a +ve int.
        """
        assert isinstance(index, int) and index >= 0
        assert isinstance(page_size, int) and page_size > 0

        indexed_dataset = self.indexed_dataset()
        dataset_size = len(indexed_dataset)

        assert index < dataset_size

        data = []
        current_index = index
        kaunt = 0

        while kaunt < page_size and current_index < dataset_size:
            if current_index in indexed_dataset:
                data.append(indexed_dataset[current_index])
                kaunt += 1
            current_index += 1

        next_index = current_index if current_index < dataset_size else None

        return {
            'index': index,
            'data': data,
            'page_size': len(data),
            'next_index': next_index
        }
