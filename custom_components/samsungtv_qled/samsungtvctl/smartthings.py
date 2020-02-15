# Smartthings TV integration

import requests
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError
import json
import os

API_BASEURL = "https://api.smartthings.com/v1"
API_DEVICES = API_BASEURL + "/devices/"
COMMAND_REFRESH = "{'commands':[{'component': 'main','capability': 'refresh','command': 'refresh'}]}"


def list_devices(api_key):
    """ Get the name and the deviceId of all TVs linked to smartthings. """
    resp = requests.get(API_DEVICES, headers={"Authorization": "Bearer " + api_key})
    data = resp.json()
    devices = data["items"]
    list_devices = [[device["label"], device["deviceId"]] for device in devices if "[TV]" in device["name"]]
    return list_devices

class SmartthingsTV:

    def __init__(self, api_key, device_id):
        self._state = "off"
        self._muted = False
        self._volume = 0
        self._api_key = api_key
        self._device_id = device_id
        self._source = ""
        self._source_list = []
        self._channel = ""
        self._channel_name = ""
        self._picture_mode = ""
        self._sound_mode = ""

    def __exit__(self, type, value, traceback):
        self.close()

    def device_update(self):
        REQUEST_HEADERS = {"Authorization": "Bearer " + self._api_key}
        DEVICE_ID = self._device_id
        API_DEVICE = API_DEVICES + DEVICE_ID
        API_DEVICE_STATUS = API_DEVICE + "/states"
        API_COMMAND = API_DEVICE + "/commands"

        # Refresh device
        requests.post(API_COMMAND,data=COMMAND_REFRESH ,headers=REQUEST_HEADERS)

        # Get new data
        resp = requests.get(API_DEVICE_STATUS,headers=REQUEST_HEADERS)
        data = resp.json()

        self._state = data['main']['switch']['value']

        if data['main']['volume']['value'] != None:
            self._volume = int(data['main']['volume']['value']) / 100
        else:
            self._volume = 0

        self._source_list = json.loads(data['main']['supportedInputSources']['value'])
        if data['main']['mute']['value'] == "mute":
            self._muted = True
        else:
            self._muted = False
        self._source =  data['main']['inputSource']['value']
        self._channel = data['main']['tvChannel']['value']
        self._channel_name = data['main']['tvChannelName']['value']
        if self._channel_name != ""  and self._channel == '':
            self._channel_name = self._channel_name.split('.')[1]
        self._picture_mode = data['main']['pictureMode']['value']
        self._supported_picture_modes = data['main']['supportedPictureModes']['value']
        self._sound_mode = data['main']['soundMode']['value']
        self._supported_sound_modes = data['main']['supportedSoundModes']['value']

    def send_command(self, command):
        requests.post("https://api.smartthings.com/v1/devices/" + self._device_id + "/commands", data=command, headers={"Authorization": "Bearer " + self._api_key})

    def turn_on(self):
        self.send_command("{'commands': [{'component': 'main','capability': 'switch','command': 'on'}]}")
    
    def turn_off(self):
        self.send_command("{'commands': [{'component': 'main','capability': 'switch','command': 'off'}]}")

    def select_source(self, source):
        self.send_command("{'commands':[{'component': 'main','capability': 'mediaInputSource','command': 'setInputSource', 'arguments': ['" + source + "']}]}")

    def play(self):
        self.send_command("{'commands':[{'component': 'main','capability': 'mediaPlayback','command': 'play'}]}")

    def pause(self):
        self.send_command("{'commands':[{'component': 'main','capability': 'mediaPlayback','command': 'pause'}]}")

    def stop(self):
        self.send_command("{'commands':[{'component': 'main','capability': 'mediaPlayback','command': 'stop'}]}")

    def volume_up(self):
        self.send_command("{'commands':[{'component': 'main','capability': 'audioVolume','command': 'volumeUp'}]}")

    def volume_down(self):
        self.send_command("{'commands':[{'component': 'main','capability': 'audioVolume','command': 'volumeDown'}]}")

    def mute(self):
        self.send_command("{'commands':[{'component': 'main','capability': 'audioMute','command': 'mute'}]}")

    def unmute(self):
        self.send_command("{'commands':[{'component': 'main','capability': 'audioMute','command': 'unmute'}]}")

    def fast_forward(self):
        self.send_command("{'commands':[{'component': 'main','capability': 'mediaPlayback','command': 'fastForward'}]}")

    def rewind(self):
        self.send_command("{'commands':[{'component': 'main','capability': 'mediaPlayback','command': 'rewind'}]}")




