import unittest
from task import main
import socket
import paho.mqtt.client as mqtt
from multiprocessing import Process
from datetime import datetime
import json


class SimpleTestCase(unittest.TestCase):

    def test_pub_sub(self):
        hostname = socket.gethostname()
        settings = {
            'mqtt_brocker_host': 'test.mosquitto.org',
            'mqtt_brocker_port': 1884,
            'mqtt_brocker_user': 'rw',
            'mqtt_brocker_password': 'readwrite'
        }

        mqtt_client = mqtt.Client()
        mqtt_client.username_pw_set(settings['mqtt_brocker_user'], settings['mqtt_brocker_password'])

        self.is_working = True

        def on_message(client, userdata, message):
            data_from_brocker = json.loads(message.payload)

            self.assertIn('cpu_temp', data_from_brocker)
            self.assertIn('cpu_freq', data_from_brocker)
            self.assertIn('cpu_load_percent', data_from_brocker)
            self.assertIn('ram_load_percent', data_from_brocker)
            self.assertIn('swap_usage', data_from_brocker)
            self.assertIn('root_fs_disk_usage', data_from_brocker)

            self.is_working = False

        def on_connect(client, userdata, flags, rc):
            mqtt_client.subscribe(f'{hostname}/sensors_data')
            p = Process(target=main, args=(settings,))
            p.start()

        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message
        mqtt_client.connect(host=settings['mqtt_brocker_host'], port=settings['mqtt_brocker_port'])

        start_time = datetime.now()
        while self.is_working:
            mqtt_client.loop()

            current_time = datetime.now()
            if (current_time - start_time).total_seconds() > 30:
                self.fail('test timeout!')


if __name__ == '__main__':
    unittest.main()
