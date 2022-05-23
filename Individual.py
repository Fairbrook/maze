from cmath import sqrt
from typing import List
from Coord import Coord


def calc_distance(start: Coord, end: Coord):
    base = end.X - start.X
    height = end.Y - start.Y
    return sqrt(base ** 2 + height ** 2).real


def calc_points_between(start: Coord, end: Coord):
    points = []
    distance = calc_distance(start, end)
    if distance == 0:
        return points

    rise = end.Y - start.Y
    run = end.X - start.X
    slope = (rise/run) if run != 0 else 0
    intercept = end.Y-slope*end.X
    if abs(slope) > 1:
        run = 0

    def next_x(x):
        if run == 0:
            return x
        step = 1 if run > 0 else -1
        return x+step

    def next_y(y, x):
        step = 1 if rise > 0 else -1
        if run == 0:
            return y+step
        return slope*x + intercept

    x = next_x(start.X)
    y = next_y(start.Y, x)
    new_point = Coord(round(x), round(y))
    return [new_point] + calc_points_between(new_point, end)


class Individual:
    def __init__(self, position=Coord(), history: List[Coord] = []) -> None:
        self.__position = position
        self.__history = history if len(history) > 0 else [position]
        pass

    def set_position(self, position: Coord) -> None:
        rounded = Coord(round(position.X), round(position.Y))
        points = calc_points_between(self.__position, rounded)
        self.__position = rounded
        for point in points:
            self.__history.append(point)
        if len(points) == 0:
            self.__history.append(rounded)
        self.__history.append(rounded)

    def get_position(self) -> Coord:
        pos = self.__position
        return Coord(pos.X, pos.Y)

    def get_history(self) -> List[Coord]:
        return self.__history

    def distance_to(self, goal: Coord) -> float:
        return calc_distance(self.__position, goal)

    def evaluate_to(self, goal: Coord) -> float:
        return self.distance_to(goal)+100*len(self.__history)
