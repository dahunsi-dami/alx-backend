#!/usr/bin/env python3
"""index_range simple helper function."""


def index_range(page: int, page_size: int) -> tuple:
    """Returns tuple of size w/ start, end index."""
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return (start_index, end_index)
