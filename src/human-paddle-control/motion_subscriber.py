# from distutils.command.config import config
import time

import paho.mqtt.client as mqtt
import numpy as np
import json
import uuid

"""
This class was removed from the driver to follow previous development patterns
"""

class MotionSubscriber:
    """
    MQTT compliant game state subscriber
    """

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        # client.subscribe("puck/position") # we can use this subscription to drive the player update rather than relying on our own loop
        # client.subscribe("player1/score")
        # client.subscribe("player2/score")
        # client.subscribe("paddle1/position")
        # client.subscribe("paddle2/position")
        client.subscribe("game/level")
        client.subscribe("game/state")

    # since we are only sending information at regular intervals this may not be needed
    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = json.loads(msg.payload)
        if topic == "game/level":
            self.level = payload["level"]
        if topic == "game/state":
            self.game_state = payload["state"]
    #     if topic == "puck/position":
            # self.puck_x = payload["x"]
            # self.puck_y = payload["y"]
            # We'll use this update to grab a player position value and then publish
        
    def publish(self, topic, message, qos=0):
        """
        Use the subscriber to send a message to update game variables elsewhere
        """
        p = json.dumps(message)
        self.client.publish(topic, payload=p, qos=qos)

    # get depth camera feed into browser
    def emit_depth_feed(self, feed):
        self.client.publish("depth/feed", payload=json.dumps({"feed": feed}))
        #print(f'emitting depth feed: {feed}')

    def __init__(self):
        self.level = 0
        self.game_state = 0
        client_id = "human-paddle-control-" + str(uuid.uuid1())
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = lambda client, userdata, flags, rc : self.on_connect(client, userdata, flags, rc)
        self.client.on_message = lambda client, userdata, msg : self.on_message(client, userdata, msg)
        # self.client.connect_async("localhost", port=1883, keepalive=60)
        # self.client.connect_async("192.168.2.214", port=1883, keepalive=60)
        self.client.connect_async("mqtt-broker", port=1883, keepalive=60)
        
    def start(self):
        self.client.loop_forever()
