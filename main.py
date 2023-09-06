"""Main file for the project."""
import os
import logging
from datetime import date

import dotenv
from pymsteams import connectorcard

from helper_objects import MessageSender

dotenv.load_dotenv()
DEV = False

HOURS_DICT = {
    "monday": {"start": "17:00", "end": "19:00"},
    "tuesday": {"start": "17:00", "end": "19:00"},
    "wednesday": {"start": "17:00", "end": "19:00"},
    "thursday": {"start": "17:00", "end": "19:00"},
    # "friday": {"start": "06:00", "end": "20:00"},
}

EXCEPTION_DICT = {
    # date(2023, 9, 6): "I will be unavailable today.",
    date(2023, 9, 15): "I will be unavailable today. Please check back tomorrow.",
}

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    connector = connectorcard(
        os.environ.get("DEV_TEAMS_WEBHOOK_URL")
        if DEV
        else os.environ.get("TEAMS_WEBHOOK_URL")
    )
    message_sender = MessageSender(connector, HOURS_DICT, EXCEPTION_DICT)
    message_sender.run(DEV)
