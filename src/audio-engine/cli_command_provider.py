"""
CLI AudioCommandProvider implementation module.
"""

from audio_command_handler import AudioCommandHandler

class CLI:
    """
    This class is the command line interface implementation of the 
    AudioCommandProvider. It recieves input from standard i/o and 
    calls a AudioCommandHandler.
    Example using docker:
    docker run --rm --device /dev/snd audio-engine -c --set text='Hello, My name is Paul.' --set filename='hello.wav' --set vm='en_US-hfc_male-medium'
    """

    def __init__(self, audio_command_handler: AudioCommandHandler):
        self.audio_command_handler = audio_command_handler

    def __command(self, text: str, filename: str, voice_model:str = "en_US-amy-medium"):
        """
        This function calls an AudioCommandHandler synchronously to synthesize and play
        a text utterance.

        Arguments:
            text -- the text utterance.
            filename -- the audio file filename.
            voice_model -- the name of the voice model to use.
        """

        self.audio_command_handler.record_tts_to_file(text, filename, voice_model)
        self.audio_command_handler.play(filename)
        self.audio_command_handler.remove_file(filename)

    def start(self, args):
        """
        This function starts recieving of audio events from the standard i/o.

        Arguments:
            args -- an implemention specific set of arguments.
        """
        required_keys={"text", "filename"}

        if args.keys() < required_keys:
            exit(1)

        text = args["text"]
        filename = args["filename"]

        if "vm" in args:
            vm = args["vm"]
        else:
            vm = "en_US-amy-medium"

        self.__command(text, filename, vm)
