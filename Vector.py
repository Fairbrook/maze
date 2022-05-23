class Vector:
    def __init__(self, x=0, y=0) -> None:
        self.X = x
        self.Y = y

    def __add__(self, v):
        if type(v) is int:
            return Vector(self.X+v, self.Y+v)

        if type(v) is float:
            return Vector(self.X+v, self.Y+v)

        return Vector(self.X+v.X, self.Y+v.Y)

    def __sub__(self, v):
        if type(v) is int:
            return Vector(self.X-v, self.Y-v)

        if type(v) is float:
            return Vector(self.X-v, self.Y-v)

        return Vector(self.X-v.X, self.Y-v.Y)

    def __mul__(self, v):
        if type(v) is int:
            return Vector(self.X*v, self.Y*v)

        if type(v) is float:
            return Vector(self.X*v, self.Y*v)

        return Vector(self.X*v.X, self.Y*v.Y)
