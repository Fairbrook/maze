
from copy import copy
from datetime import datetime
from time import time
from typing import List
from PIL import Image
from Coord import Coord

from Pixel import Pixel

image_path = "maze.png"
initial_point = (0, 199)


def get_pixels(path: str) -> List[List[Pixel]]:
    bytearray = []
    with Image.open(path) as img:
        width, _ = img.size
        row = []
        for pixel in list(img.getdata()):
            r, g, b, _ = pixel
            row.append(Pixel(r, g, b))
            if len(row) >= width:
                bytearray.append(row)
                row = []
        # if len(row) > 0:
        #     bytearray.append(row)
    return bytearray


# def get_valid_children(coords: tuple, maze: list) -> list:
#     x, y = coords
#     possible_coords = []
#     if x > 0:
#         possible_coords.append((x-1, y))
#     if x < len(maze[y])-1:
#         possible_coords.append((x+1, y))
#     if y > 0:
#         possible_coords.append((x, y-1))
#     if y < len(maze)-1:
#         possible_coords.append((x, y+1))
#     return list(filter(lambda coord: get_color(maze[coord[1]][coord[0]]) != 'black', possible_coords))


def draw_path(path: List[Coord], image: list):
    image_copy = copy(image)
    color = 100
    for coord in path:
        image_copy[coord.Y][coord.X] = Pixel(255, 0, 255)
    return image_copy


def matrix_to_img(matrix: List[List[Pixel]]):
    matrix_copy = copy(matrix)
    image = []
    for row in matrix_copy:
        for pixel in row:
            byte = (pixel.red, pixel.green, pixel.blue, 0xFF)
            image.extend(byte)
    return bytes(image)


def show_result(path: list, image: list):
    size = len(image)
    img = Image.frombytes('RGBA', (size, size),
                          matrix_to_img(draw_path(path, image)))
    # img.show()
    filename = f"{datetime.today()}".split('.')[0].replace(":", "-")
    img.save(f"results/{filename}.png")
