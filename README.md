# SamsungTV custom component
This is a custom component compatible with Samsung QLED TVs. 
This is still a work in progress and sometimes you might have issues.
To get all features you must connect your TV to Smartthings.<br/>
This component is inspired by the work of @xchwarze, @jaruba and @pegatron89.

# Features

- Turn ON/OFF (WOL, KEY input ot Smartthings)
- Return State (ping TV or Smartthings)
- Send KEY
- Get current source (Smartthings)
- Change source (Smartthings)
- Set and get volume value
- Launch applications
- Applications can be set as sources
- Play music and video from an url
- Get audio profile

**What the component can't do:**
- change audio profile (yet)
- change video profile
- lots of remote KEYs can't be used on QLED TVs

# Installation (manual)
1. Download the ``custom_components`` folder
2. Copy the ``samsungtv_qled`` folder within your ``custom_components`` folder in your ``config`` directory.
Your ``config`` directory should look like the following.

````
└── configuration.yaml
└── custom_components
    └── samsungtv_qled
        └── samsungtvctl
        └── __init__.py
        └── manifest.json
        └── media_player.py
````

# Configuration

Edit your configuration.yaml file and reboot HA to enable the component.

```
# Example configuration.yaml entry
media_player:
  - platform: samsungtv_qled
    host: IP_ADDRESS
    port: PORT
    name: Samsung TV
    mac: MAC_ADDRESS
    update_method: 'smartthings'
    app_list: '{"Netflix": "11101200001", "Youtube": "111299001912", "Apple TV": "3201807016597", "Plex": "3201512006963", "Prime Video": "3201512006785"}'
    api_key: 'SMARTTHINGS_API_KEY'
    device_id: 'SMARTTHINGS_DEVICE_ID'

```
**host (required):** Ip address of your TV.

**port (optional):** If you don't want to use 8002.

**name (optional):** Name of your TV.

**mac (optional):** Required to turn on the TV.

**update_method (optional):** Change the ping method used for state update. Values: "default", "ping", "smartthings". <br/>Smartthings seems to be more accurate.

**update_custom_ping_url (optional):** Custom endpoint to ping. Only if update_method is "ping".<br/>Recommanded value: "http://IP_ADDRESS:9197/dmr"

**app_list (optional)**: Apps visible in the dropdown source menu.<br/>
Default value: AUTOGENERATED<br/>
Example value: '{"Netflix": "11101200001", "YouTube": "111299001912", "Spotify": "3201606009684"}'

**api_key (optional):** Smartthings api token.<br/> You can generate a token here: https://account.smartthings.com/tokens

**device_id (optional, required if api_key):** Your TV device_id in Smartthings.<br/>
Go to https://graph-eu01-euwest1.api.smartthings.com/device/list and select on your TV.
Your device_id is in the address bar: 
https://graph-eu01-euwest1.api.smartthings.com/device/show/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX

# Usage

### Send Keys
```
service: media_player.play_media
```

```json
{
  "entity_id": "media_player.samsungtv",
  "media_content_type": "send_key",
  "media_content_id": "KEY_CODE",
}
```
**Note**: Change "KEY_CODEKEY" by desired key_code.

Script example:
```
tv_channel_down:
  alias: Channel down
  sequence:
  - service: media_player.play_media
    data:
      entity_id: media_player.samsung_tv55
      media_content_id: KEY_CHDOWN
      media_content_type: "send_key"
```
### Cast to TV

`service: media_player.play_media`

```
{
  "entity_id": "media_player.samsungtv",
  "media_content_type": "url",
  "media_content_id": "FILE_URL",
}
```
_Replace FILE_URL with the url of your file._