from typing import List
from Individual import calc_points_between
from Pixel import Pixel
from Coord import Coord
OBSTACLE = Pixel(0, 0, 0)
START = Pixel(0, 0, 0xFF)
GOAL = Pixel(0, 0xFF, 0)


class Map:
    def __init__(self, pixels: List[List[Pixel]]) -> None:
        self.pixels = pixels

    def get_starting_coords(self):
        coords = []
        for y, row in enumerate(self.pixels):
            for x, pixel in enumerate(row):
                if pixel == START:
                    coords.append(Coord(x, y))
        return coords

    def get_goal_coords(self):
        for y, row in enumerate(self.pixels):
            for x, pixel in enumerate(row):
                if pixel == GOAL:
                    return Coord(x+3, y+3)

    def get_possible_movements(self, from_pos: Coord):
        valid_moves: List[Coord] = []
        if from_pos.X > 0:
            valid_moves.append(Coord(from_pos.X-1, from_pos.Y))
        if from_pos.Y > 0:
            valid_moves.append(Coord(from_pos.X, from_pos.Y-1))
        if from_pos.X < len(self.pixels)-1:
            valid_moves.append(Coord(from_pos.X+1, from_pos.Y))
        if from_pos.X < len(self.pixels)-1:
            valid_moves.append(Coord(from_pos.X, from_pos.Y+1))

        return list(filter(lambda coord: self.pixels[coord.Y][coord.X] != OBSTACLE, valid_moves))

    def is_position_valid(self, position: Coord):
        if position.Y >= len(self.pixels) or position.Y < 0:
            return False
        if position.X >= len(self.pixels[0]) or position.X < 0:
            return False
        return self.pixels[position.Y][position.X] != OBSTACLE

    def last_valid_position(self, start: Coord, end: Coord):
        points = calc_points_between(start, end)
        for point in points:
            if self.is_position_valid(point):
                return point
        return start
