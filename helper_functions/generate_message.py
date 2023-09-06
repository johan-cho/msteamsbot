"""Generate a message based on the end time."""

import random
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


def generate_message(end_time: str) -> str:
    """Generate a message based on the end time.

    Args:
        end_time: The end time of the current hour.
    Returns:
        A message based on the end time.
    """

    return (
        random.choice(HELLO_ARRAY) + ", my name is Johan Cho, "
        "and I tutor in Engineer Database Systems (and *maybe* another class). "
        "I'll be available until " + format_time_str(end_time) + " EST. "
        "Please send your name and question or assignment! "
    )
