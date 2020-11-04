import json
import os
from renjuu.managers.const import default_dict


def json_save(filename, data):
    with open(filename, 'w+') as file:
        json.dump(data, file)


def json_load(filename):
    check_path_exist(filename)
    with open(filename, 'r') as file:
        return json.load(file)


def check_path_exist(filename):
    if not os.path.exists(filename):
        json_save(filename, default_dict)


def save(filename, text):
    with open(filename, 'w+') as file:
        file.write(text)
