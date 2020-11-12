import os
import json

from renjuu.game.const import Color


class Scoreboard:
    def __init__(self, filename):
        self.filename = filename

    @staticmethod
    def parse_data(data):
        text = "Score table\n"
        for key in data:
            text += "%s : %s \n" % (key, data[key])
        return text

    @staticmethod
    def stat_increment(data: dict, win_color: Color, players: list):
        if win_color == Color.non:
            for player in players:
                data[player.color.name] += 1
        else:
            data[win_color.name] += 2

    @staticmethod
    def json_save(filename, data):
        with open(filename, 'w+') as file:
            json.dump(data, file)

    def json_load(self, filename):
        self.check_path_exist(filename)
        with open(filename, 'r') as file:
            return json.load(file)

    def check_path_exist(self, filename):
        if not os.path.exists(filename):
            self.json_save(filename,
                           {color.name: 0 for color in Color
                            if color is not Color.non})

    @staticmethod
    def save(filename, text):
        with open(filename, 'w+') as file:
            file.write(text)

    def update_stat(self, game):
        data = self.json_load(self.filename + ".json")
        self.stat_increment(data, game.winner, game.players)
        text = self.parse_data(data)
        self.json_save(self.filename + ".json", data)
        self.save(self.filename + ".txt", text)
