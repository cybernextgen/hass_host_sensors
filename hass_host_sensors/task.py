#!/usr/bin/env python3
from typing import Any, Dict, Union
import paho.mqtt.publish as publish
import logging
import sys
import psutil
import socket
import json

SETTINGS = {
    'mqtt_brocker_host': 'localhost',
    'mqtt_brocker_port': 1883,
    'mqtt_brocker_user': '',
    'mqtt_brocker_password': ''
}

logger = logging.getLogger(__name__)


def main(settings: Dict['str', Union[str, int]]) -> None:
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(fmt="%(asctime)s %(name)s.%(levelname)s: %(message)s", datefmt="%Y.%m.%d %H:%M:%S")

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    try:
        sensors_data = read_data_from_sensors()
        send_sensors_data_to_brocker(sensors_data, settings)
    except Exception as e:
        logger.exception(e)


def read_data_from_sensors() -> Dict[str, Union[str, int, float]]:
    cpu_temp = 0
    sensors_data = psutil.sensors_temperatures()
    if 'coretemp' in sensors_data:
        cpu_temp_sensors = sensors_data['coretemp']
        if len(cpu_temp_sensors) > 0:
            cpu_temp = sensors_data['coretemp'][0].current
    else:
        logger.warning('coretemp not present in sensors data!')

    cpu_freq = round(psutil.cpu_freq().current, 1)
    cpu_load_percent = psutil.cpu_percent(interval=1)

    ram_load_percent = psutil.virtual_memory().percent
    swap_usage = psutil.swap_memory().percent
    root_fs_disk_usage = psutil.disk_usage('/').percent
    return {'cpu_temp': cpu_temp,
            'cpu_freq': cpu_freq,
            'cpu_load_percent': cpu_load_percent,
            'ram_load_percent': ram_load_percent,
            'swap_usage': swap_usage,
            'root_fs_disk_usage': root_fs_disk_usage}


def send_sensors_data_to_brocker(sensors_data: Dict[str, Any], settings: Dict['str', Union[str, int]]) -> None:
    host_name = socket.gethostname()
    sensors_data_json = json.dumps(sensors_data)
    publish.single(f'{host_name}/sensors_data',
                   hostname=settings.get('mqtt_brocker_host'),
                   payload=sensors_data_json,
                   port=settings.get('mqtt_brocker_port'),
                   auth={'username': settings.get('mqtt_brocker_user'),
                         'password': settings.get('mqtt_brocker_password')})


if __name__ == '__main__':
    main(SETTINGS)
