class Coord:
    def __init__(self, X=0, Y=0) -> None:
        self.X = X
        self.Y = Y
        pass

    def __eq__(self, __o: object) -> bool:
        if __o == None:
            return False
        return self.X == __o.X and self.Y == __o.Y

    def __sub__(self, v):
        return Coord(self.X-v.X, self.Y-v.Y)

    def __add__(self, v):
        return Coord(self.X+v.X, self.Y+v.Y)

    def __mul__(self, v):
        if type(v) is int:
            return Coord(self.X*v, self.Y*v)

        if type(v) is float:
            return Coord(self.X*v, self.Y*v)

        return Coord(self.X*v.X, self.Y*v.Y)
