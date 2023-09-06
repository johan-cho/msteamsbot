"""Generate a message based on the end time."""

import random
from datetime import date

from .format_time_str import format_time_str

HELLO_ARRAY = [
    "Hello",
    "Hi",
    "Hey",
    "Yo",
    "Sup",
    "Howdy",
    "Greetings",
    "Hiya",
    "Heya",
    "Heyo",
]


def generate_message(end_time: str, exceptions: dict[date, str] = None) -> str:
    """Generate a message based on the end time.

    Args:
        end_time: The end time of the current hour.
    Returns:
        A message based on the end time.
    """

    for date_key, message in exceptions.items():
        if date.today() == date_key:
            return message

    return (
        random.choice(HELLO_ARRAY) + ", my name is Johan Cho, "
        "and I primarily tutor in Engineer Database Systems. "
        "I'll be available until " + format_time_str(end_time) + " EST. "
        "Please send your name and question or assignment! "
    )
