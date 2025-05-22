"""
TTSSynthesizer Interface definition module.
"""

from typing import Protocol

class TTSSynthesizer(Protocol):
    """
    This protocol class defines the interface for all TTS synthesizers.
    Implementations of this interface will recieve a text utterance and
    synthesize it to a wave file.
    """

    def synthesize_to_file(self, text: str, filename: str, voice_model: str):
        """
        Implementations of this function synthesize a text utterance into
        a wave audio file based on a specified voice model. 

        Arguments:
            text -- the text utterance.
            filename -- the audio file filename.
            voice_model -- the name of the voice model to use.
        """
    def remove_file(self, filename: str):
        """
        Implementations of this function removes a generated audio
        file.

        Arguments:
            filename -- the audio file filename.
        """
