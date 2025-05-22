"""
AudioEngine/main module.
"""
import os
import logging
import argparse
from piper_tts_synthesizer import PiperTTSSynthesizer
from simpleaudio_audio_player import SimpleaudioAudioPlayer

# from vlc_audio_player import VLCAudioPlayer
from controller import Controller
from tts_synthesizer import TTSSynthesizer
from audio_player import AudioPlayer
from audio_command_provider import AudioCommandProvider
from audio_command_handler import AudioCommandHandler
from mqtt_command_provider import MQTT
from cli_command_provider import CLI

logging.basicConfig(level=logging.INFO)

class AudioEngine(object):
    """
    This class implements the entry point for the audio engine. It instantiates, 
    and manages the composition of the engine components then starts the system. 
    """

    def __init__(self, data_path: str, cli: bool = False, extra_args=None):
        self.data_path = data_path

        logging.debug("data_path: %s", self.data_path)

        # TTS synthesizer.
        self.tts_synthesizer: TTSSynthesizer = PiperTTSSynthesizer(self.data_path)

        # Audio player.
        self.audio_player: AudioPlayer = SimpleaudioAudioPlayer(self.data_path)
        # self.audio_player = VLCAudioPlayer(self.data_path)

        # Audio command handler.
        self.audio_command_handler: AudioCommandHandler = Controller(
            self.data_path, self.tts_synthesizer, self.audio_player
        )

        # Audio command producer.
        if cli:
            self.audio_command_provider: AudioCommandProvider = CLI(self.audio_command_handler)
        else:
            self.audio_command_provider: AudioCommandProvider = MQTT(self.audio_command_handler)

        self.audio_command_provider.start(extra_args)


class ParseDict(argparse.Action):
    """
    This class manages the 'set' command line parameters. 
    """

    def __call__(self, parser, namespace, values, option_string=None):
        d = getattr(namespace, self.dest) or {}

        if values:
            for item in values:
                split_items = item.split("=", 1)
                key = split_items[
                    0
                ].strip()  # we remove blanks around keys, as is logical
                value = split_items[1]

                d[key] = value

        setattr(namespace, self.dest, d)


def main():
    """
    This class manages the command line parameters. 
    
    """
    description = """\
        synopsis:
        .
    """
    
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--data-path", 
        default="data",
        help="Path to store audio files."
    )
    parser.add_argument(
        "-c",
        "--cli",
        action="store_true",
        help="Use command line interface.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print messages during actions.",
    )
    parser.add_argument(
        "--set",
        metavar="KEY=VALUE",
        nargs="+",
        help="Set a number of key-value pairs "
        "(do not put spaces before or after the = sign). "
        "If a value contains spaces, you should define "
        "it with double quotes: "
        'foo="this is a sentence". Note that '
        "values are always treated as strings.",
        action=ParseDict,
    )
    options = parser.parse_args()

    if not os.path.exists(options.data_path):
        os.makedirs(options.data_path)

    AudioEngine(options.data_path, options.cli, options.set)


if __name__ == "__main__":
    main()
