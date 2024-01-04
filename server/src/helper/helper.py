"""
MODULE contains helper functions for server.py
"""


def parse_datetime(datetime: str):
    """
    Separate date and time from string
    datetime: string
    return: string
    """
    return datetime.replace("_", " ")
