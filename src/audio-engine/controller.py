"""
Default AudioCommandHandler implementation module.
"""

from threading import Thread
from tts_synthesizer import TTSSynthesizer
from audio_player import AudioPlayer

class Controller:
    """
    This class is the default implementation of the AudioCommandHandler. 
    It recieves calls from a AudioCommandProvider and manages the orchestration
    flow between the system components when an audio command is invoked.
    """

    def __init__(
        self, data_path: str, tts_synthesizer: TTSSynthesizer, audio_player: AudioPlayer
    ):
        self.done = False
        self.data_path = data_path
        self.tts_synthesizer = tts_synthesizer
        self.audio_player = audio_player

    def record_tts_to_file(self, text: str, filename: str, voice_model: str):
        """
        This function implements a synchronous command to synthesize a text 
        utterance into a wave audio file based on a specified voice model.  

        Arguments:
            text -- the text utterance.
            filename -- the audio file filename.
            voice_model -- the name of the voice model to use.
        """
        self.tts_synthesizer.synthesize_to_file(text, filename, voice_model)

    def play(self, filename: str):
        """
        This function implements a synchronous command to play and audio file.  

        Arguments:
            filename -- the audio file filename.
        """
        self.audio_player.play(filename)

    def stop(self, filename: str):
        """
        This function implements a synchronous command to stop a playing audio file.  

        Arguments:
            filename -- the audio file filename.
        """
        self.audio_player.stop(filename)

    def remove_file(self, filename: str):
        """
        This function implements a synchronous command to stop a playing audio file.  

        Arguments:
            filename -- the audio file filename.
        """
        self.tts_synthesizer.remove_file(filename)

    def record_tts_to_file_async(
        self,
        text: str,
        filename: str,
        voice_model: str,
    ):
        """
        This function implements an asynchronous command to synthesize a text 
        utterance into a wave audio file based on a specified voice model.  

        Arguments:
            text -- the text utterance.
            filename -- the audio file filename.
            voice_model -- the name of the voice model to use.
        """
        Thread(
            target=self.record_tts_to_file,
            args=(
                text,
                filename,
                voice_model,
            ),
        ).start()

    def play_async(self, filename: str):
        """
        This function implements an asynchronous command to play and audio file.  

        Arguments:
            filename -- the audio file filename.
        """
        Thread(target=self.play, args=(filename,)).start()

    def stop_async(self, filename: str):
        """
        This function implements an asynchronous command to stop a playing audio file.  

        Arguments:
            filename -- the audio file filename.
        """
        Thread(
            target=self.stop,
            args=(filename,),
        ).start()

    def remove_file_async(self, filename: str):
        """
        This function implements an asynchronous command to stop a playing audio file.  

        Arguments:
            filename -- the audio file filename.
        """
        Thread(
            target=self.remove,
            args=(filename,),
        ).start()
