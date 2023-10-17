"""Message sender class."""
import logging
from typing import Self
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
        connector_card (connectorcard): The connector card to send messages to.
    """

    def __init__(self, connector_card: connectorcard) -> None:
        """Initialize the message sender.

        Args:
            connector_card (connectorcard): The connector card to send messages to.
        """

        super().__init__()
        self.connector_card = connector_card
        logging.info("MessageSender connected to %s", connector_card.hookurl)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.connector_card.hookurl})"

    def __str__(self) -> str:
        return str(self.connector_card.payload) + "\n" + str(self.jobs)

    def schedule(
        self,
        interval: str,
        *args,
        at: str = None,
        every: int = None,
        tz: str = "America/New_York",
        inplace: bool = True,
        **kwargs,
    ) -> Self | None:
        """Schedule a message to be sent every interval.

        Args:
            interval (str): The interval to send the message.
            at (str): The time to send the message, defaults to None.
            every (int): The amount of times to send the message, defaults to None.
            tz (str): The timezone to send the message, defaults to "America/New_York".
            inplace (bool): Whether to return the message sender instance, defaults to True.
        Returns:
            Self: The message sender instance. None if inplace is False.
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
            job.at(at or "00:00", tz=tz).do(
                threader, self.send_message, *args, join=True, **kwargs
            )
        else:
            job = getattr(self.every(every), interval)
            job.do(threader, self.send_message, *args, join=True, **kwargs)
        logging.info("Scheduled %s", job)
        if not inplace:
            return self

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
