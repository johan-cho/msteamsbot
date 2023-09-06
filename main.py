"""Main file for the project."""
import os
import logging
import dotenv

from pymsteams import connectorcard

from helper_objects import MessageSender


HOURS_DICT = {
    "monday": {"start": "06:00", "end": "20:00"},
    "tuesday": {"start": "06:00", "end": "20:00"},
    "wednesday": {"start": "13:00", "end": "20:00"},
    "thursday": {"start": "06:00", "end": "20:00"},
    "friday": {"start": "06:00", "end": "20:00"},
}


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    dotenv.load_dotenv()
    CONNECTOR = connectorcard(os.environ.get("TEAMS_WEBHOOK_URL"))
    message_sender = MessageSender(CONNECTOR, HOURS_DICT)
    message_sender.run()
