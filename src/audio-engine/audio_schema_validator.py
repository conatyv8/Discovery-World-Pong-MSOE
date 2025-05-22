"""
AudioSchemaValidator module.
"""
import logging
import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError

class AudioSchemaValidator:
    """
    This class defines the validates JSON messages recieved by JSON based
    AudioCommandProviders.
    """

    def __init__(self):
        with open("schema/tts_schema.json", encoding="utf-8") as f:
            self.tts_schema = json.load(f)

        with open("schema/play_schema.json", encoding="utf-8") as f:
            self.play_schema = json.load(f)

        with open("schema/stop_schema.json", encoding="utf-8") as f:
            self.stop_schema = json.load(f)

        with open("schema/remove_schema.json", encoding="utf-8") as f:
            self.remove_schema = json.load(f)

    def validate_tts(self, json_data):
        """
        This function validates TTS command messages.

        Arguments:
            json_data -- the JSON data recieved.
        """
        try:
            validate(instance=json_data, schema=self.tts_schema)
        except ValidationError as e:
            self.__log(e, self.get_play_schema())
            return False
        return True

    def validate_play(self, json_data):
        """
        This function validates Play command messages.

        Arguments:
            json_data -- the JSON data recieved.
        """
        try:
            validate(instance=json_data, schema=self.play_schema)
        except ValidationError as e:
            self.__log(e, self.get_play_schema())
            return False
        return True

    def validate_stop(self, json_data):
        """
        This function validates Stop command messages.

        Arguments:
            json_data -- the JSON data recieved.
        """
        try:
            validate(instance=json_data, schema=self.stop_schema)
        except ValidationError as e:
            self.__log(e, self.get_stop_schema())
            return False
        return True

    def validate_remove(self, json_data):
        """
        This function validates Remove command messages.

        Arguments:
            json_data -- the JSON data recieved.
        """
        try:
            validate(instance=json_data, schema=self.remove_schema)
        except ValidationError as e:
            self.__log(e, self.get_remove_schema())
            return False
        return True

    def get_tts_schema(self):
        """
        This function returns the TTS message schema.
        """
        return json.dumps(self.tts_schema, indent=4)

    def get_play_schema(self):
        """
        This function returns the Play message schema.
        """
        return json.dumps(self.play_schema, indent=4)

    def get_stop_schema(self):
        """
        This function returns the Stop message schema.
        """
        return json.dumps(self.stop_schema, indent=4)

    def get_remove_schema(self):
        """
        This function returns the Remove message schema.
        """
        return json.dumps(self.remove_schema, indent=4)

    def __log(self, e, schema):
        """Function printing python version."""
        logging.info("Invalid JSON data: %s", e.message)
        logging.info("JSON schema: %s", schema)
