"""
AudioPlayer Interface definition module.
"""

from typing import Protocol

class AudioPlayer(Protocol):
    """
    This protocol class defines the interface for all audio players.
    Implementations of this interface will manage the playing of audio
    files.
    """

    def play(self, filename: str):
        """
        Implementations of this function plays an audio file.

        Arguments:
            filename -- the audio file filename.
        """

    def stop(self, filename: str):
        """
        Implementations of this function stops a currently playing audio
        file.

        Arguments:
            filename -- the audio file filename.
        """
