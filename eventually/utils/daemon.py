"""
Database cleaner daemon
=======================

The module that provides daemon for removing the inactive users from db.
"""

# pylint: disable=wrong-import-position

import argparse
import datetime
import os
import time
import sys
import django

SOURCE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SOURCE_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eventually.settings")
django.setup()

from authentication.models import CustomUser
from authentication.views import TTL_SEND_PASSWORD_TOKEN as TTL_ACTIVATION
from utils.utils import LOGGER

class Daemon():
    """Daemon class that provides basic functionality for creating more specify daemon utils."""

    def __init__(self, frequency):
        """
        Method that initializes the new Daemon instance.

        :param self: the current Daemon instance.
        :type self: object

        :param frequency: the time between two sequences of run method firing.
        :type frequency: int

        :param is_processed: defines the state of the daemon executing process.
        :type is_processed: bool
        """

        self.is_processed = True
        self.frequency = frequency

    def start(self):
        """
        Method that runs when some Daemon instance start to process user-defined commands.

        :param self: the current Daemon instance.
        :type self: object

        :return: None
        """

        print('Daemon was successfully started')

    def stop(self):
        """
        Method that runs when some Daemon instance stop to process user-defined commands.

        :param self: the current Daemon instance.
        :type self: object

        :return: None
        """

        print('Daemon was successfully stopped')

    def run(self):
        """
        Method that implements permanent repetition for the execute method.

        :param self: the current Daemon instance.
        :type self: object

        :return: None
        """

        self.start()
        while self.is_processed:
            self.execute()
            time.sleep(self.frequency)
        self.stop()

    def execute(self):
        """Method that has to be overloaded and defines the certain commands for execution."""

        raise NotImplementedError


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

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('frequency',
                        type=int,
                        help='amount of seconds between two sequences of daemon execute method.')
    GROUP = PARSER.add_mutually_exclusive_group()
    GROUP.add_argument('-M',
                       '--minutes',
                       action='store_true',
                       help='flag that determines the frequency parameter as number of minutes.')
    GROUP.add_argument('-H',
                       '--hours',
                       action='store_true',
                       help='flag that determines the frequency parameter as number of hours.')
    ARGS = PARSER.parse_args()

    ARG_FREQUENCY = ARGS.frequency
    if ARGS.minutes:
        ARG_FREQUENCY = ARGS.frequency * 60
    elif ARGS.hours:
        ARG_FREQUENCY = ARGS.frequency * 60 * 60

    EVENTUALLY_DB_CLEANER = DatabaseCleaner(ARG_FREQUENCY)
    EVENTUALLY_DB_CLEANER.run()
