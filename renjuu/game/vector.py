class Vector(tuple):
    @property
    def x(self):
        return super().__getitem__(0)

    @property
    def y(self):
        return super().__getitem__(1)

    def __hash__(self):
        return super().__hash__()

    def __add__(self, other):
        return Vector([self.x + other.x, self.y + other.y])

    def __sub__(self, other):
        return Vector([self.x - other.x, self.y - other.y])

    def __mul__(self, other: int):
        return Vector([self.x * other, self.y * other])

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __neg__(self):
        return Vector([-self.x, -self.y])
