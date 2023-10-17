"""Main file for the project."""
import os
import time
import logging
import argparse
from datetime import date
from typing import NoReturn, Any
import dotenv
from pymsteams import connectorcard

from helper_objects import MessageSender
from helper_functions import generate_message, format_time_str

# pylint: disable=line-too-long
dotenv.load_dotenv()
ARGPARSE = argparse.ArgumentParser()

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


def add_arg(parser: argparse.ArgumentParser, _arg: str, *args, **kwargs) -> Any:
    """Add arguments to the argument parser.

    Args:
        parser (argparse.ArgumentParser): The argument parser to add the argument to.
        _arg (str): The name of the argument to add.
    """
    parser.add_argument(f"--{_arg}", *args, **kwargs)
    arg_result = getattr(parser.parse_args(), _arg)
    logging.info("Argument %s set to %s", _arg, arg_result)
    return arg_result


def main(dev: bool) -> NoReturn | None:
    """Main function for the project.

    Args:
        dev (bool): Whether or not to run in development mode.
    """

    message_sender_list: list[MessageSender] = []
    for weekday, message in HOURS_DICT.items():
        message_sender = MessageSender(
            connectorcard(
                os.environ.get("DEV_TEAMS_WEBHOOK_URL")
                if dev
                else os.environ.get("TEAMS_WEBHOOK_URL")
            )
            .addLinkButton("Check In", os.environ.get("FORMS_URL"))
            .text(generate_message((weekday, message), EXCEPTION_DICT))
            .title(
                f"IE3425 {weekday.capitalize()} Tutoring {format_time_str(message['start'])} - {format_time_str(message['end'])}"
            )
        )
        if dev:
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
    dev_mode = add_arg(
        ARGPARSE,
        "dev",
        help="Whether or not to run in dev mode.",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    main(dev=dev_mode)
