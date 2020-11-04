from renjuu.game.const import Color
from renjuu.managers.const import string_colors


def stat_constructor(data):
    text = "Score table\n"
    for key in data:
        text += "%s : %s \n" % (key, data[key])
    return text


def stat_inc(data, win_color, players):
    if win_color == Color.non:
        for player in players:
            data[string_colors[player.color]] += 1
    else:
        data[string_colors[win_color]] += 2
