def get_coordinates(x, y):
    x_pos = (x * 32) + 160
    y_pos = (y * 32) + 65
    return x_pos, y_pos


def info_inc(x):
    temp = int(x.info)
    if temp < 8:
        temp += 1
        x.info = str(temp)


def info_dec(x):
    temp = int(x.info)
    if temp > 2:
        temp -= 1
        x.info = str(temp)
