import sys 
import math 
import functools 
from enum import Enum 

class Color(Enum):
    RED = 1
    GREEN = 2

class Board:
    def __init__(self: Board) -> None:
        self.tiles: dict[dict[Color]] = { }
        self.tiles_rev: dict[dict[Color]] = { }

    def get_tile(self: Board, x: int, y: int) -> Color | None:
        if x not in self.tiles:
            return None 
        
        x_dict = self.tiles[x]

        if y not in x_dict:
            return None 
        
        return x_dict[y]
    
    @functools.cache
    def get_tile_cached(self: Board, x: int, y: int) -> Color | None:
        return self.get_tile(x, y)

    def add(self: Board, x: int, y: int, color: Color) -> None:
        if self.get_tile(x, y) != None:
            return 
            # assert False, f"Error: tried to add a tile @ {x}, {y} which was already in the board!"

        if x not in self.tiles:
            self.tiles[x] = { }

        if y not in self.tiles_rev:
            self.tiles_rev[y] = { }

        self.tiles[x][y] = color
        self.tiles_rev[y][x] = color 

    def create_greens(self: Board) -> None:
        largest_x = max(x for x in self.tiles.keys()) + 1
        largest_y = max(x for x in self.tiles_rev.keys()) + 1

        print(f"{largest_x=} {largest_y=}")

        # For each row, grab each red tile, and fill in the tiles between with green tiles 
        print(f"Filling rows 0 -> {largest_y}...")
        for y in range(largest_y):
            if y not in self.tiles_rev:
                continue 

            curr_tiles = {key: value for key, value in self.tiles_rev[y].items() if value == Color.RED}

            if len(curr_tiles) == 0:
                continue 

            min_x = min(x for x in curr_tiles.keys())
            max_x = max(x for x in curr_tiles.keys())

            for x in range(min_x + 1, max_x):
                self.add(
                    x, 
                    y,
                    Color.GREEN
                )

        # self.print()
        # print("")

        # For each column, grab each red tile, and fill in the tiles between with green tiles 
        print(f"Filling columns 0 -> {largest_x}...")
        for x in range(largest_x):
            if x not in self.tiles:
                continue 

            curr_tiles = {key: value for key, value in self.tiles[x].items() if value == Color.RED}

            if len(curr_tiles) == 0:
                continue 

            min_y = min(x for x in curr_tiles.keys())
            max_y = max(x for x in curr_tiles.keys())

            for y in range(min_y + 1, max_y):
                self.add(
                    x, 
                    y,
                    Color.GREEN
                )

        # self.print()
        # print("")

        # Fill in the shape: on each row, find the first and last tile, and fill the unfilled
        # tiles between them with green tiles 
        print(f"Filling interior 0 -> {largest_y}...")
        for y in range(largest_y):
            if (y % 1000) == 0:
                print(f"-> {y=}")

            if y not in self.tiles_rev:
                continue 

            curr_tiles = {key: value for key, value in self.tiles_rev[y].items()}

            if len(curr_tiles) == 0:
                continue 

            curr_tiles = { k: self.tiles_rev[y][k] for k in sorted(self.tiles_rev[y]) }

            first_tile = next(iter(curr_tiles))
            last_tile = next(reversed(curr_tiles))

            # Could optimize in some cases? 
            # if self.tiles[first_tile][y] == Color.RED and self.tiles[last_tile][y] == Color.RED:
            #     continue 

            for x in range(first_tile + 1, last_tile):
                # if self.get_tile(x, y) != None:
                #     continue 
                
                self.add(
                    x,
                    y,
                    Color.GREEN
                )

                # self.print()
                # print("")

        # self.print()
        # print("")

    def all_areas(self: Board) -> list[(int, int, Color)]:
        areas = [ ]

        @functools.cache 
        def area(x1, y1, x2, y2) -> int:
            x_dim = x1 - x2 if x1 > x2 else x2 - x1 
            y_dim = y1 - y2 if y1 > y2 else y2 - y1

            x_dim += 1
            y_dim += 1

            return x_dim * y_dim 

        for x1 in self.tiles.keys():
            for y1 in self.tiles[x1].keys():
                color1 = self.tiles[x1][y1]

                if color1 != Color.RED:
                    continue 

                for x2 in self.tiles.keys():
                    for y2 in self.tiles[x2].keys():
                        color2 = self.tiles[x2][y2]

                        if color2 != Color.RED:
                            continue 

                        if x1 == x2 and y1 == y2:
                            continue 

                        corner1 = x1, y2
                        corner2 = x2, y1 

                        if self.get_tile_cached(corner1[0], corner1[1]) == None:
                            continue 

                        if self.get_tile_cached(corner2[0], corner2[1]) == None:
                            continue 

                        areas.append((
                            x1,
                            y1,
                            x2,
                            y2,
                            area(x1, y1, x2, y2)
                        ))

        return areas 

    def print(self: Board):
        largest_x = max(x for x in self.tiles.keys()) + 3
        largest_y = max(y for y in self.tiles_rev.keys()) + 2

        for y in range(largest_y):
            for x in range(largest_x):
                tile = self.get_tile(x, y)

                if tile == None:
                    print('.', end = '')
                    continue 

                if tile == Color.RED:
                    print('#', end = '')
                    continue 

                if tile == Color.GREEN:
                    print('X', end = '')
                    continue 

            print('')

# class Tile:
#     def __init__(self: Tile, x: int, y: int, color: Color):
#         self.x = x
#         self.y = y 
#         self.color = color 

#     def __str__(self: Tile) -> str:
#         return f"Tile: {self.x}, {self.y}"

#     @functools.cache 
#     def distance_to(self: Tile, tile: Tile) -> float:
#         return math.sqrt(pow(self.x - tile.x, 2) + pow(self.y - tile.y, 2))

#     @functools.cache 
#     def area(self: Tile, tile: Tile) -> int:
#         x_dim = self.x - tile.x if self.x > tile.x else tile.x - self.x 
#         y_dim = self.y - tile.y if self.y > tile.y else tile.y - self.y

#         x_dim += 1
#         y_dim += 1

#         return x_dim * y_dim 

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

board = Board()

all_tiles = [ ]

print(f"Creating board...")

for line in lines:
    line = line.strip('\n')

    parts = line.split(',')

    board.add(
        int(parts[0], 10),
        int(parts[1], 10),
        Color.RED
    )

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
areas = sorted(areas, key = lambda x: x[4], reverse=True)

for i in range(min(10, len(areas))):
    x1, y1, x2, y2, area = areas[i]

    print(f"t1: {x1}, {y1}, t2: {x2} {y2}, area: {area}")

# t1, t2, area = areas[0][0], areas[0][1], areas[0][2]

# print(f"t1: {t1}, t2: {t2}, area: {area}")

# for tile in all_tiles:
#     print(tile)