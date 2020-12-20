import json
import os


def load_settings(filename: str):
    check_path_exist(filename)
    with open(filename, 'r') as file:
        return json.load(file)


def check_path_exist(filename: str):
    if not os.path.exists(filename):
        with open(filename, 'w+') as file:
            json.dump({'self-ip': '127.0.0.1',
                       'conn-ip': '127.0.0.1',
                       'self-port': 50000,
                       'conn-port': 50000, 'name': None}, file)
