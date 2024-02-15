"""Main file for the project."""

import argparse
import logging
import os
import threading
import time
from datetime import date
from typing import Any, NoReturn

import dotenv

from helper_functions import format_time_str, generate_message
from helper_objects import MessageSender

# pylint: disable=line-too-long


def main(
    dev: bool,
    hours_dict: dict[str, dict[str, str]],
    exception_dict: dict[date, str] = None,
) -> NoReturn | None:
    """Main function for the project.

    Args:
        dev (bool): Whether or not to run in development mode.
        hours_dict (dict[str, dict[str, str]]): The dictionary of hours to send messages at.
        exception_dict (dict[date, str]): The dictionary of exceptions to the normal message.
    """

    message_sender_list: list[MessageSender] = []
    for weekday, message in hours_dict.items():
        message_sender = (
            MessageSender(
                os.environ.get("DEV_TEAMS_WEBHOOK_URL")
                if dev
                else os.environ.get("TEAMS_WEBHOOK_URL")
            )
            .addLinkButton("Check In", os.environ.get("FORMS_URL"))
            .text(generate_message((weekday, message), exception_dict))
            .title(
                f"IE3425 {weekday.capitalize()} Tutoring {format_time_str(message['start'])} - {format_time_str(message['end'])}"
            )
        )
        if dev:
            message_sender.schedule("seconds", every=10)
        else:
            message_sender.schedule(weekday, at=message["start"])
        message_sender_list.append(message_sender)

    run_senders(*message_sender_list)


def run_senders(*senders: MessageSender, delay: int = 5) -> NoReturn | None:
    """Start the message senders.

    Args:
        senders (list[MessageSender]): The list of message senders to start.
        delay (int): The delay between each message sender starting.
    """

    worker_thread = threading.Thread(target=MessageSender.worker_main)
    worker_thread.start()

    while True:
        for sender in senders:
            sender.run_pending()
            time.sleep(delay)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    dotenv.load_dotenv()
    ARGPARSE = argparse.ArgumentParser()
    ARGPARSE.add_argument(
        "--dev",
        action="store_true",
        help="Run in development mode.",
    )
    HOURS_DICT = {
        "monday": {"start": "17:45", "end": "19:00"},
        "tuesday": {"start": "17:45", "end": "19:00"},
        "wednesday": {"start": "17:45", "end": "19:00"},
        "thursday": {"start": "17:45", "end": "19:00"},
        "friday": {"start": "14:00", "end": "19:00"},
    }
    EXCEPTION_DICT = {
        date(
            2023, 10, 18
        ): "I'm biking to a co-op meeting in watertown and I can't make tutoring today, however, I will try to respond asap if anything comes up.",
    }

    main(ARGPARSE.parse_args().dev, HOURS_DICT, EXCEPTION_DICT)
