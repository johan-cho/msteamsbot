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
    # "Howdy",
    # "Greetings",
    "Hiya",
    "Heya",
    "Heyo",
]

ROOM_DICT = {
    "monday": "Squatting in a room near Richards 155 if you want to meet in person.",
    "wednesday": "Squatting in a room near Ryder 156 if you want to meet in person.",
    "thursday": "Squatting in a room somewhere in Behrakis if you want to meet in person.",
}


def generate_message(
    time_tuple: tuple[str, dict[str, str]], exceptions: dict[date, str] = None
) -> str:
    """Generate a message based on the end time.

    Args:
        time_tuple (tuple[str, dict[str, str]]): The tuple of the day and the dictionary of the start and end times, formatted by ("wednesday", {"start": "06:00", "end": "20:00"}).
        exceptions (dict[date, str]): The dictionary of exceptions to the message, formatted by {date: "message"}.
    Returns:
        A message based on the end time.
    """

    execptions = exceptions or {}

    return (
        execptions[date.today()]
        if date.today() in execptions
        else (
            f"{random.choice(HELLO_ARRAY)}, my name is Johan Cho "
            "and I primarily tutor in Engineer Database Systems. "
            f"I'm available until {format_time_str(time_tuple[1]['end'])} EST. "
            f"I'm {ROOM_DICT.get(time_tuple[0], ' virtual today.')} "
            "Reply to this with your name and question or assignment, "
            "then check in (button below) and join the meeting! "
        )
    )
