class Point:
    def __init__(self, x, y, color):
        self.X = x
        self.Y = y
        self.color = color
        self.lines = []

    def __eq__(self, other):
        return self.X == other.X\
               and self.Y == other.Y \
               and self.color == other.color

    def __ne__(self, other):
        return self.X != other.X\
               or self.Y != other.Y \
               or self.color != other.color
