import os
import json
import requests

APP_URL_FORMAT = "http://{}:8001/api/v2/applications/{}"

APPS = {'YouTube': '111299001912',
        'Plex': '3201512006963',
        'Prime Video': '3201512006785',
        'Netflix': '11101200001',
        'Apple TV': '3201807016597',
        'Spotify': '3201606009684',
        'Google Play': '3201601007250',
        }


class Application:
    """ Handle applications."""
    def __init__(self, config):
        self._ip = config['host']
    
    def state(self, app):
        """ Get the state of the app."""
        try:
            response = requests.get(APP_URL_FORMAT.format(self._ip, APPS[app]), timeout=0.2)
            return response.content.decode('utf-8')
        except:
            return """{"id":"","name":"","running":false,"version":"","visible":false}"""

    def is_running(self, app):
        """ Is the app running."""
        app_state = json.loads(self.state(app))
        return app_state['running']

    def is_visible(self, app):
        """ Is the app visible."""
        app_state = json.loads(self.state(app))
        return app_state['visible']
    
    def start(self, app):
        """ Start an application."""
        return os.system("curl -X POST " + APP_URL_FORMAT.format(self._ip, APPS[app]))
    
    def stop(self, app):
        """ Stop an application."""
        return os.system("curl -X DELETE " + APP_URL_FORMAT.format(self._ip, APPS[app]))

    def current_app(self):
        """ Get the current visible app."""
        current_app = None
        for app in APPS:
            if (self.is_visible(app) is True):
                current_app = app
        return current_app

    def app_list(self):
        """ List running apps."""
        apps = []
        for app in APPS:
            if (self.is_running(app) is True):
                apps.append(app)
        return apps
