import sys 
import math 
import functools 
from enum import Enum 

class Color(Enum):
    RED = 1
    GREEN = 2

class Board:
    def __init__(self: Board) -> None:
        self.tiles = [ ]

    def get_tile(self: Board, x: int, y: int) -> Tile | None:
        for tile in self.tiles:
            if tile.x == x and tile.y == y:
                return tile 
            
        return None 

    @functools.cache
    def get_tile_cached(self: Board, x: int, y: int) -> Tile | None:
        return self.get_tile(x, y)

    def add(self: Board, tile: Tile) -> None:
        if tile in self.tiles:
            return

        if self.get_tile(tile.x, tile.y) != None:
            assert False, f"Error: tried to add a tile @ {tile.x}, {tile.y} which was already in the board!"

        self.tiles.append(tile)

    def create_greens(self: Board) -> None:
        largest_x = max(x.x for x in self.tiles) + 1
        largest_y = max(x.y for x in self.tiles) + 1

        # For each row, grab each red tile, and fill in the tiles between with green tiles 
        print(f"Filling rows 0 -> {largest_y}...")
        for y in range(largest_y):
            if (y % 1000) == 0:
                print(f"{y=}")

            curr_tiles = [tile for tile in self.tiles if tile.y == y and tile.color == Color.RED]

            if len(curr_tiles) == 0:
                continue 

            min_x = min(x.x for x in curr_tiles)
            max_x = max(x.x for x in curr_tiles)

            for x in range(min_x + 1, max_x):
                self.add(Tile(
                    x, 
                    y,
                    Color.GREEN
                ))

        # For each column, grab each red tile, and fill in the tiles between with green tiles 
        print(f"Filling columns 0 -> {largest_x}...")
        for x in range(largest_x):
            curr_tiles = [tile for tile in self.tiles if tile.x == x and tile.color == Color.RED]

            if len(curr_tiles) == 0:
                continue 

            min_y = min(x.y for x in curr_tiles)
            max_y = max(x.y for x in curr_tiles)

            for y in range(min_y + 1, max_y):
                self.add(Tile(
                    x, 
                    y,
                    Color.GREEN
                ))

        # Fill in the shape: on each row, find the first and last tile, and fill the unfilled
        # tiles between them with green tiles 
        print(f"Filling interior 0 -> {largest_y}...")
        for y in range(largest_y):
            curr_tiles = [tile for tile in self.tiles if tile.y == y]

            if len(curr_tiles) == 0:
                continue 

            curr_tiles = sorted(curr_tiles, key = lambda x: x.x)

            first_tile = curr_tiles[0]
            last_tile = curr_tiles[-1]

            for x in range(first_tile.x + 1, last_tile.x):
                if self.get_tile(x, y) != None:
                    continue 
                
                self.add(Tile(
                    x,
                    y,
                    Color.GREEN
                ))

    def all_areas(self: Board) -> list[Tile]:
        areas = [ ]

        red_tiles = [x for x in self.tiles if x.color == Color.RED]

        for i, tile1 in enumerate(red_tiles):
            for tile2 in red_tiles[i + 1:]:
                # Before adding, we must check that the opposite corners of the 
                # rectangle are still within the grid 

                corner1 = tile1.x, tile2.y
                corner2 = tile2.x, tile1.y 

                if self.get_tile_cached(corner1[0], corner1[1]) == None:
                    continue 

                if self.get_tile_cached(corner2[0], corner2[1]) == None:
                    continue 

                areas.append((
                    tile1,
                    tile2,
                    tile1.area(tile2)
                ))

        return areas 

    def print(self: Board):
        largest_x = max(x.x for x in self.tiles) + 3
        largest_y = max(x.y for x in self.tiles) + 2

        for y in range(largest_y):
            for x in range(largest_x):
                tile = self.get_tile(x, y)

                if tile == None:
                    print('.', end = '')
                    continue 

                if tile.color == Color.RED:
                    print('#', end = '')
                    continue 

                if tile.color == Color.GREEN:
                    print('X', end = '')
                    continue 

            print('')

class Tile:
    def __init__(self: Tile, x: int, y: int, color: Color):
        self.x = x
        self.y = y 
        self.color = color 

    def __str__(self: Tile) -> str:
        return f"Tile: {self.x}, {self.y}"

    @functools.cache 
    def distance_to(self: Tile, tile: Tile) -> float:
        return math.sqrt(pow(self.x - tile.x, 2) + pow(self.y - tile.y, 2))

    @functools.cache 
    def area(self: Tile, tile: Tile) -> int:
        x_dim = self.x - tile.x if self.x > tile.x else tile.x - self.x 
        y_dim = self.y - tile.y if self.y > tile.y else tile.y - self.y

        x_dim += 1
        y_dim += 1

        return x_dim * y_dim 

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

board = Board()

all_tiles = [ ]

print(f"Creating board...")

for line in lines:
    line = line.strip('\n')

    parts = line.split(',')

    new_tile = Tile(
        int(parts[0], 10),
        int(parts[1], 10),
        Color.RED
    )

    board.add(new_tile)

# print(f"Initial board:")
# board.print()

print(f"Creating greens...")
board.create_greens()

# print("")

# print(f"Updated board:")
# board.print()

print(f"Calculating areas...")
areas = board.all_areas()

print(f"Sorting areas...")
areas = sorted(areas, key = lambda x: x[2], reverse=True)

for i in range(10):
    tile1, tile2, dist = areas[i]

    print(f"t1: {tile1}, t2: {tile2}, area: {dist}")

# t1, t2, area = areas[0][0], areas[0][1], areas[0][2]

# print(f"t1: {t1}, t2: {t2}, area: {area}")

# for tile in all_tiles:
#     print(tile)