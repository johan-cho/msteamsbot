"""Main file for the project."""
import os
import time
import logging
from datetime import date
from typing import NoReturn
import dotenv
from pymsteams import connectorcard

from helper_objects import MessageSender
from helper_functions import generate_message, format_time_str

# pylint: disable=line-too-long
dotenv.load_dotenv()
DEV = False

HOURS_DICT = {
    "monday": {"start": "17:45", "end": "19:00"},
    "tuesday": {"start": "17:45", "end": "19:00"},
    "wednesday": {"start": "17:45", "end": "19:00"},
    "thursday": {"start": "17:45", "end": "19:00"},
    "friday": {"start": "14:00", "end": "19:00"},
}

EXCEPTION_DICT: dict = {
    date(
        2023, 10, 18
    ): "I'm biking to a co-op meeting in watertown and I can't make tutoring today, however, I will try to respond asap if anything comes up.",
}


def main() -> NoReturn | None:
    """Main function for the project."""

    message_sender_list: list[MessageSender] = []
    for weekday, message in HOURS_DICT.items():
        message_sender = MessageSender(
            connectorcard(
                os.environ.get("DEV_TEAMS_WEBHOOK_URL")
                if DEV
                else os.environ.get("TEAMS_WEBHOOK_URL")
            )
            .addLinkButton("Check In", os.environ.get("FORMS_URL"))
            .text(generate_message((weekday, message), EXCEPTION_DICT))
            .title(
                f"IE3425 {weekday.capitalize()} Tutoring {format_time_str(message['start'])} - {format_time_str(message['end'])}"
            )
        )
        if DEV:
            message_sender.schedule("seconds", every=10)
        else:
            message_sender.schedule(weekday, at=message["start"])
        message_sender_list.append(message_sender)

    run_senders(message_sender_list)


def run_senders(senders: list[MessageSender], delay: int = 5) -> NoReturn | None:
    """Start the message senders.

    Args:
        senders (list[MessageSender]): The list of message senders to start.
        delay (int): The delay between each message sender starting.
    """

    while senders:
        for sender in senders:
            sender.run_pending()
        time.sleep(delay)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main()
