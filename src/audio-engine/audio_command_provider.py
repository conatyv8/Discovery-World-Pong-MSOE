"""
AudioCommandProvider Interface definition module.
"""

from typing import Protocol


class AudioCommandProvider(Protocol):
    """
    This protocol class defines the interface for all audio command providers.
    Implementations of this interface will recieve command events and from a
    particular i/o type and invoked a AudioCommandHandler implementation.
    """

    def start(self, args):
        """
        Implementations of this function start the recieving of audio i/o events.

        Arguments:
            args -- an implemention specific set of arguments.
        """
