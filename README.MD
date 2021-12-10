# HASS host sensors
[![Build Status](https://api.travis-ci.com/cybernextgen/hass_host_sensors.svg?branch=master)](https://app.travis-ci.com/github/cybernextgen/hass_host_sensors) [![codecov](https://codecov.io/gh/cybernextgen/hass_host_sensors/branch/master/graph/badge.svg?token=HIYA4I77A5)](https://codecov.io/gh/cybernextgen/hass_host_sensors)

Simple MQTT interface for hass.io (HomeAssistant) host sensors. It runs as systemd service. Every `RestartSec` interval service 
will publish JSON to topic `{host_name}/sensors_data`. Fields are presented below:
```js
{
    'cpu_temp': {float, one decimal place, celsius},
    'cpu_freq': {float, one decimal place, MHz},
    'cpu_load_percent': {float, one decimal place, percent},
    'ram_load_percent': {float, one decimal place, percent},
    'swap_usage': {float, one decimal place, percent},
    'root_fs_disk_usage': {float, one decimal place, percent}
}
```

## Installation
Required python version >= 3.6

Step 1. Download source
```sh
$ git clone https://github.com/cybernextgen/hass_host_sensors.git
$ cd hass_host_sensors
$ pip install -r hass_host_sensors/requirements.txt
```
Step 2. Edit configuration constants inside `task.py` module:
```python
SETTINGS = {
    'mqtt_brocker_host': 'localhost',
    'mqtt_brocker_port': 1883,
    'mqtt_brocker_user': '',
    'mqtt_brocker_password': ''
}
```
Inside `hass_host_sensor.service` edit next lines:
```sh
ExecStart = {path to python3} {path to task.py}
User = {user} # run service as specific user and group
Group = {user group}
...
RestartSec = 60 # interval between sensors data reads
```
Step 3. Enable and run service
```sh
$ cp hass_host_sensors.service /etc/systemd/system/hass_host_sensors.service
$ systemctl enable hass_host_sensors
$ systemctl start hass_host_sensors
# show logs
$ journalctl -u hass_host_sensors.service
```