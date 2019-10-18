from samsungctl import exceptions
from samsungctl import Remote

config = {
    "host": 'YOUR_IP',
    "name": "samsungctl",
    "description": "PC",
    "id": "",
    "method": "websocket",
    "port": 8002,
    "timeout": 10
}

remote = Remote(config)

print(remote.get_installed_apps())