"""
AudioCommandHandler Interface definition module.
"""

from typing import Protocol


class AudioCommandHandler(Protocol):
    """
    This protocol class defines the interface for all audio command handlers.
    Implementations of this interface will manage the orchestrate flow between
    the system when a command is invoked. It will typically be invoked from an
    implementation of the AudioCommandProvider interface.
    """

    def record_tts_to_file(self, text: str, filename: str, voice_model: str):
        """
        Implementations of this function provide a synchronous command to
        synthesize a text utterance into a wave audio file based on a specified
        voice model.

        Arguments:
            text -- the text utterance.
            filename -- the audio file filename.
            voice_model -- the name of the voice model to use.
        """

    def play(self, filename: str):
        """
        Implementations of this function provide a synchronous command to
        play and audio file.

        Arguments:
            filename -- the audio file filename.
        """

    def stop(self, filename: str):
        """
        Implementations of this function provide a synchronous command to
        stop a playing audio file.

        Arguments:
            filename -- the audio file filename.
        """

    def remove_file(self, filename: str):
        """
        Implementations of this function provide a synchronous command to
        remove a wave audio file.

        Arguments:
            filename -- the audio file filename.
        """

    def record_tts_to_file_async(self, text: str, filename: str, voice_model: str):
        """
        Implementations of this function provide an asynchronous command to
        synthesize a text utterance into a wave audio file based on a specified
        voice model.

        Arguments:
            text -- the text utterance.
            filename -- the audio file filename.
            voice_model -- the name of the voice model to use.
        """

    def play_async(self, filename: str):
        """
        Implementations of this function provide an asynchronous command to
        play and audio file.

        Arguments:
            filename -- the audio file filename.
        """

    def stop_async(self, filename: str):
        """
        Implementations of this function provide an asynchronous command to
        stop a playing audio file.

        Arguments:
            filename -- the audio file filename.
        """

    def remove_file_async(self, filename: str):
        """
        Implementations of this function provide an asynchronous command to
        remove a wave audio file.

        Arguments:
            filename -- the audio file filename.
        """
