"""Message sender class."""
from __future__ import annotations

import logging
from queue import Queue
from typing import Self, Type

from pymsteams import connectorcard
from schedule import Job, Scheduler


class MessageSender(Scheduler, connectorcard):
    """Message sender class.

    Attributes:

        connector_card (connectorcard): The connector card to send messages to.
        jobs (list[Job]): The jobs scheduled to send messages.
    """

    jobqueue = Queue()

    @classmethod
    def worker_main(cls: Type[MessageSender]) -> None:
        """Worker main function."""
        while True:
            job_func = cls.jobqueue.get()
            job_func()
            cls.jobqueue.task_done()

    def __init__(self, webhook_url: str, **kwargs) -> None:
        """Initialize the message sender.

        Args:
            webhook_url (str): The webhook url to send messages to.
            **kwargs: The keyword arguments to pass to the connector card.
        """
        Scheduler.__init__(self)
        connectorcard.__init__(self, webhook_url, **kwargs)
        logging.info("MessageSender connected to %s", webhook_url)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.hookurl})"

    def __str__(self) -> str:
        return str(self.payload) + "\n" + str(self.jobs)

    def schedule(  # pylint: disable=too-many-arguments
        self,
        interval: str,
        at: str = None,
        every: int = None,
        tz: str = "America/New_York",
        inplace: bool = True,
    ) -> Self | None:
        """Schedule a message to be sent every interval.

        Args:
            interval (str): The interval to send the message.
            at (str): The time to send the message, defaults to None.
            every (int): The number of intervals to wairt, defaults to None.
            tz (str): The timezone to send the message, defaults to "America/New_York".
            inplace (bool): Whether to return the message sender instance, defaults to True.
        Returns:
            Self: The message sender instance. None if inplace is False.
        """
        job: Job = getattr(self.every(every or 1), interval)
        if not every:
            job.at(at or "00:00", tz=tz).do(__class__.jobqueue.put, self.send_message)
        else:
            job.do(__class__.jobqueue.put, self.send_message)
        logging.info("Scheduled %s", job)
        if not inplace:
            return self
        return None

    def send_message(self) -> None:
        """Send the connector card."""
        try:
            self.send()
            logging.info("Message: %s sent to %s", self.payload["text"], self.hookurl)
        except Exception as error:  # pylint: disable=broad-except
            logging.error("Error sending message: %s", error)
