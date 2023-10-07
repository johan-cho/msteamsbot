"""Message sender class."""
import time
import logging
import weakref
from typing import NoReturn
from typing_extensions import Self
import dotenv
from schedule import Job, Scheduler
from pymsteams import connectorcard

from helper_functions import threader

# pylint: disable=broad-except
# pylint: disable=line-too-long

dotenv.load_dotenv()


class MessageSender(Scheduler):
    """Message sender class.

    Attributes:
        instances (list[Self]): The list of instances of the message sender.
        connector_card (connectorcard): The connector card to send messages to.
    """

    instances: list[Self] = []

    def __init__(self, connector_card: connectorcard) -> None:
        """Initialize the message sender.

        Args:
            connector_card (connectorcard): The connector card to send messages to.
        """

        super().__init__()
        self.connector_card = connector_card
        self.__class__.instances.append(weakref.proxy(self))
        logging.info("MessageSender connected to %s", connector_card.hookurl)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.connector_card.hookurl})"

    def schedule(
        self,
        interval: str,
        *args,
        at: str = None,
        every: int = None,
        tz: str = "America/New_York",
    ) -> None:
        """Schedule a message to be sent every interval.

        Args:
            interval (str): The interval to send the message.
            at (str): The time to send the message, defaults to None.
            every (int): The amount of times to send the message, defaults to None.
            tz (str): The timezone to send the message, defaults to "America/New_York".
        """

        if interval in [
            "second",
            "minute",
            "hour",
            "day",
            "week",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]:
            job: Job = getattr(self.every(), interval)
            job.at(at or "00:00", tz=tz).do(threader, self.send_message, True, *args)
        else:
            job = getattr(self.every(every), interval)
            job.do(threader, self.send_message, True, *args)

    def run(self, __all: bool = False, delay: int = 5) -> NoReturn:
        """Run the message sender.

        Args:
            dev (bool): Whether to run in development mode, defaults to False.
            delay (int): The delay between checks, defaults to 5."""
        while True:
            time.sleep(delay)
            if __all:
                for __inst in self.__class__.instances:
                    __inst.run_pending()
            else:
                self.run_pending()

    def send_message(self) -> None:
        """Send the connector card."""
        try:
            self.connector_card.send()
        except Exception as error:
            logging.error("Error sending message: %s", error)
        logging.info(
            "Message: %s sent to %s",
            self.connector_card.payload["text"],
            self.connector_card.hookurl,
        )
