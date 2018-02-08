"""
Amazons cleaner daemon
=======================

The module that provides daemon for removing the inactive images from amazons3 bucket.
"""

# pylint: disable=wrong-import-position

import os
import sys
import django
from helper import arg_parcer # pylint: disable=import-error
from base_daemon import Daemon # pylint: disable=import-error


SOURCE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SOURCE_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eventually.settings")
django.setup()

from utils.awss3_helper import delete_images_awss3
from utils.utils import LOGGER

class AmazonsCleaner(Daemon):
    """Daemon class that provides removing inactive images from amazons3 bucket."""

    def __init__(self, frequency):
        """
        Method that initializes the new AmazonsCleaner instance.

        :param self: the current AmazonsCleaner instance.
        :type self: object

        :param frequency: the time between two sequences of run method firing.
        :type frequency: int
        """
        super(AmazonsCleaner, self).__init__(frequency)
        self.pid = None

    def start(self):
        """
        Method that runs when some AmazonsCleaner instance start to process user-defined commands.

        :param self: the current Daemon instance.
        :type self: object

        :return: None
        """
        self.pid = os.getpid()
        message = f'AmazonsCleaner was successfully started with pid={self.pid}'
        print(message)
        LOGGER.info(message)

    def execute(self):
        """
        Method that specifies database cleaning command.

        :param self: the current Daemon instance.
        :type self: object

        :return: None
        """
        deleted_images = delete_images_awss3()
        LOGGER.info(str(deleted_images) + " images DELETED from amazons")


if __name__ == '__main__':
    ARG_FREQUENCY = arg_parcer()
    EVENTUALLY_AMAZONS_CLEANER = AmazonsCleaner(ARG_FREQUENCY)
    EVENTUALLY_AMAZONS_CLEANER.run()
