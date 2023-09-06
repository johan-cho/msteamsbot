"""Main file for the project."""
import os
import logging
from datetime import date

import dotenv
from pymsteams import connectorcard

from helper_objects import MessageSender

dotenv.load_dotenv()
CONNECTOR = connectorcard(os.environ.get("TEAMS_WEBHOOK_URL"))

HOURS_DICT = {
    "monday": {"start": "06:00", "end": "20:00"},
    "tuesday": {"start": "06:00", "end": "20:00"},
    "wednesday": {"start": "13:00", "end": "20:00"},
    "thursday": {"start": "06:00", "end": "20:00"},
    "friday": {"start": "06:00", "end": "20:00"},
}

EXCEPTION_DICT = {
    date(2023, 9, 6): "I will be unavailable today.",
    date(2023, 9, 15): "I will be unavailable today.",
}

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    message_sender = MessageSender(CONNECTOR, HOURS_DICT, EXCEPTION_DICT)
    message_sender.run()
