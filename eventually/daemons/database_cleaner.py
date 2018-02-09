"""
Database cleaner daemon
=======================

The module that provides daemon for removing the inactive users from database.
"""

# pylint: disable=wrong-import-position

import datetime
import os
import sys
import django
from base_daemon import Daemon # pylint: disable=import-error
from helper import arg_parcer # pylint: disable=import-error


SOURCE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SOURCE_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eventually.settings")
django.setup()

from authentication.models import CustomUser
from authentication.views import TTL_SEND_PASSWORD_TOKEN as TTL_ACTIVATION
from utils.utils import LOGGER


class DatabaseCleaner(Daemon):
    """Daemon class that provides removing inactive users from database."""

    def __init__(self, frequency):
        """
        Method that initializes the new DatabaseCleaner instance.

        :param self: the current DatabaseCleaner instance.
        :type self: object

        :param frequency: the time between two sequences of run method firing.
        :type frequency: int
        """

        super(DatabaseCleaner, self).__init__(frequency)
        self.pid = None

    def start(self):
        """
        Method that runs when some DatabaseCleaner instance start to process user-defined commands.

        :param self: the current Daemon instance.
        :type self: object

        :return: None
        """

        self.pid = os.getpid()
        message = f'Eventually database cleaner was successfully started with pid={self.pid}'
        print(message)
        LOGGER.info(message)

    def execute(self):
        """
        Method that specifies database cleaning command.

        :param self: the current Daemon instance.
        :type self: object

        :return: None
        """

        users = CustomUser.objects.filter(is_active=False)
        for user in users:
            if user.created_at.timestamp() + TTL_ACTIVATION < datetime.datetime.now().timestamp():
                if user.delete_by_id(user.id):
                    LOGGER.info(f'pid={self.pid} user {user} was successfully removed.')
                else:
                    LOGGER.info(f'pid={self.pid} user {user} doesn\'t exist')


if __name__ == '__main__':
    ARG_FREQUENCY = arg_parcer()
    EVENTUALLY_DB_CLEANER = DatabaseCleaner(ARG_FREQUENCY)
    EVENTUALLY_DB_CLEANER.run()
