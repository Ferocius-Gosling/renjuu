import enum


class RequestType(enum.IntEnum):
    CURRENT_PLAYERS = 1
    BEGIN = 2
    MOVE = 3
    EXIT = 4
    RESTART = 5
    CONNECTING = 6


class RequestParams(enum.IntEnum):
    TYPE = 1
    PLAYERS = 2
    MOVE = 3
    NAME = 4
    ID = 5
    MAX_PLAYERS = 6
