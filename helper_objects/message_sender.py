"""Message sender class."""
import time
import logging
from datetime import date
from typing import NoReturn
from schedule import Job, Scheduler
from pymsteams import connectorcard

from helper_functions import generate_message, format_time_str, threader

# pylint: disable=broad-except


class MessageSender(Scheduler):
    """Message sender class.

    Attributes:
        connector_card: The connector card to send messages to.
        hours_dict: The dictionary of hours to send messages.
    """

    BUTTON_MESSAGE = "Click here to fill out the form."
    BUTTON_URL = "https://forms.office.com/r/MMhJWEC2LW"

    def __init__(
        self,
        connector_card: connectorcard,
        hours_dict: dict[dict[str, str]],
        exceptions: dict[date, str] = None,
    ):
        """Initialize the message sender.

        Args:
            connector_card: The connector card to send messages to.
            hours_dict: The dictionary of hours to send messages.
            exceptions: The dictionary of exceptions to the message.
        """

        super().__init__()
        self.connector_card = connector_card.addLinkButton(
            MessageSender.BUTTON_MESSAGE, MessageSender.BUTTON_URL
        )
        self.hours_dict = hours_dict
        self.exceptions = exceptions or {}

        logging.info("MessageSender connected to %s", connector_card.hookurl)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.connector_card.hookurl}, {self.hours_dict})"

    def run(self) -> NoReturn:
        """Run the message sender."""
        for time_tuple in self.hours_dict.items():
            # self.every().minute.do(self.threader, self.send_message, True, time_tuple)
            job: Job = getattr(self.every(), time_tuple[0])
            job.at(time_tuple[1]["start"], tz="America/New_York").do(
                threader, self.send_message, True, time_tuple[1]["end"]
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
