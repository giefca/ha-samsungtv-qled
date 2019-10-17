# SamsungTV custom component
This is a custom component compatible with Samsung QLED TVs. 
(It was developped to work with my 2018 Q9FN and never had been tested with an other TV.)
Older TVs should still work but won't have the new features.

This is still a work in progress and sometimes you might have issues.

# Features

- Turn ON/OFF
- return State (still a small issue, the TV state turn back on in HA 1 minute after turned off and turn off 1 minute later)
- send KEY
- set and get volume
- launch applications
- applications can be set as sources, HA knows if you are using an app on your TV
- launch streaming of music and video from files (not compatible with HA stream component)

**What the component can't do:**
- differentiate TV from HDMI sources, it will show TV/HDMI
- switch to a diffent HDMI source (QLED TVs do not respond to older remote commands)
- change audio and video profile
- lot of remote KEYs can't be used on QLED TVs

# Installation
1. Download the ``custom_components`` folder
2. Copy the ``samsungtv_qled`` folder within your ``custom_components`` folder in your ``config`` directory.
Your ``config`` directory should look like the following.

````
└── configuration.yaml
└── custom_components
    └── samsungtv_qled
        └── samsungctl
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
    port: PORT (8002 for QLED)
    name: Samsung TV
    mac: MAC_ADDRESS
    applist: "YouTube, Apple TV, Plex, Prime Video, Spotify" (only for QLED)
    timeout: 5
```
**port:** 8002 for QLED

**mac:** required to turn on the TV

**applist (optional)**: list of the apps you want in the source drop down menu
(YouTube, Plex, Prime Video, Universal Guide, Netflix, Apple TV, Steam Link, MyCANAL, Spotify, Molotov, SmartThings, e-Manual, Google Play, Gallery, Rakuten TV, RMC Sport, MYTF1 VOD, Blacknut, Facebook Watch, McAfee Security for TV, OCS, Playzer)

**timeout:** DO NOT set it too low or you won't have enough time to authorize HA on your TV on the first activation

# Usage

## Send KEY
```
service: media_player.play_media
```
```
{
  "entity_id": "media_player.samsungtv",
  "media_content_type": "key",
  "media_content_id": "KEY_CODE",
}
```

## Launch application
You can use the source droplist or service ``media_player.select_source`` to launch one of the applications of your configuration file.

To launch an other application you must use the ``media_player.play_media`` service.
```
service: media_player.play_media
```
```
{
  "entity_id": "media_player.samsungtv",
  "media_content_type": "app",
  "media_content_id": "Application name",
}
```
**Compatible applications (case sensitive):** YouTube, Plex, Prime Video, Universal Guide, Netflix, Apple TV, Steam Link, MyCANAL, Spotify, Molotov, SmartThings, e-Manual, Google Play, Gallery, Rakuten TV, RMC Sport, MYTF1 VOD, Blacknut, Facebook Watch, McAfee Security for TV, OCS, Playzer.

## Launch media file
```
service: media_player.play_media
```
```
{
  "entity_id": "media_player.samsungtv",
  "media_content_type": "url",
  "media_content_id": "MEDIA_URL",
}
```
