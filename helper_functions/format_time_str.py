"""Formats a time string to a more readable format."""
import logging


def format_time_str(time_str: str) -> str:
    """Format the time string.

    Args:
        time_str: The time string to format.
    Returns:
        The formatted time string.
    """

    try:
        time_array = time_str.split(":")

        hours = int(time_array[0])
        minutes = time_array[1].zfill(2)
    except ValueError:
        logging.error("Invalid time string: %s", time_str)
        return time_str

    return (
        str(hours - 12) + ":" + minutes + " PM"
        if hours > 12
        else str(hours) + ":" + minutes + " AM"
    )
