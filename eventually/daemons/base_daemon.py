"""
Base daemon
=======================

The module that provides base Daemon class.
"""

# pylint: disable=wrong-import-position

import time


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
