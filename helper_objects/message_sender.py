"""Message sender class."""
import os
import time
import logging
from datetime import date
from typing import NoReturn
import dotenv
from schedule import Job, Scheduler
from pymsteams import connectorcard

from helper_functions import generate_message, format_time_str, threader

# pylint: disable=broad-except

dotenv.load_dotenv()


class MessageSender(Scheduler):
    """Message sender class.

    Attributes:
        connector_card: The connector card to send messages to.
        hours_dict: The dictionary of hours to send messages.
        exceptions: The dictionary of exceptions to the message.
    """

    FORMS_BUTTON_MESSAGE = "Check In"
    TEAMS_BUTTON_MESSAGE = "Join Meeting"

    def __init__(
        self,
        connector_card: connectorcard,
        hours_dict: dict[dict[str, str]],
        exceptions: dict[date, str] = None,
    ) -> None:
        """Initialize the message sender.

        Args:
            connector_card (connectorcard): The connector card to send messages to.
            hours_dict (dict[dict[str, str]]): The dictionary of hours to send messages, formatted by {"wednesday", {"start": "06:00", "end": "20:00"}.
            exceptions (dict[date, str]): The dictionary of exceptions to the message, formatted by {date: "message"}.
        """

        super().__init__()
        self.connector_card = connector_card.addLinkButton(
            MessageSender.FORMS_BUTTON_MESSAGE, os.environ.get("FORMS_URL")
        ).addLinkButton(MessageSender.TEAMS_BUTTON_MESSAGE, os.environ.get("TEAMS_URL"))
        self.hours_dict = hours_dict
        self.exceptions = exceptions or {}

        logging.info("MessageSender connected to %s", connector_card.hookurl)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.connector_card.hookurl}, {self.hours_dict})"

    def run(self, dev: bool = False) -> NoReturn:
        """Run the message sender.

        Args:
            dev (bool): Whether to run in development mode, defaults to False."""
        for time_tuple in self.hours_dict.items():
            if dev:
                self.every().minute.do(threader, self.send_message, True, time_tuple)
                continue
            job: Job = getattr(self.every(), time_tuple[0])
            job.at(time_tuple[1]["start"], tz="America/New_York").do(
                threader, self.send_message, True, time_tuple
            )

        while True:
            self.run_pending()
            time.sleep(1)

    def send_message(self, time_tuple: tuple[str, dict[str, str]]) -> None:
        """Send a message to the user.

        Args:
            end_time: The end time of the current hour.
        """
        message_text = generate_message(time_tuple[1]["end"], self.exceptions)
        teams_message = self.connector_card.text(message_text).title(
            f"IE3425 {time_tuple[0].capitalize()} Tutoring {format_time_str(time_tuple[1]['start'])} - {format_time_str(time_tuple[1]['end'])}"
        )
        try:
            teams_message.send()
        except Exception as error:
            logging.error("Error sending message: %s", error)

        logging.info("Message: %s sent to %s", message_text, teams_message.hookurl)
