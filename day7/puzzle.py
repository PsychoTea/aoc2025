import sys 
import functools 
from typing import Tuple 

CHAR_START = 'S'
CHAR_SPLITTER = '^'
CHAR_BEAM = '|'
CHAR_EMPTY = '.'

class Splitter:
    all: list[Splitter] = [ ]

    def __init__(self: Splitter, input: list[str], x: int, y: int) -> Splitter:
        self.x = x
        self.y = y

        self.left = None 
        self.right = None 

        self._calculate(input)

        Splitter.all.append(self)

    # Create a splitter, given the input data, and x and y position
    # If a given splitter already exists at that location, return it 
    @classmethod
    def Create(cls: Splitter, input: list[str], x: int, y: int) -> Splitter:
        if found_node := cls.Find(x, y):
            return found_node 
        
        return Splitter(input, x, y)

    # Find a splitter at a given x and y position
    @classmethod 
    def Find(cls: Splitter, x: int, y: int) -> Splitter:
        return next((node for node in cls.all 
                     if node.x == x and node.y == y), None)
    
    # Count the total number of splitters 
    @classmethod 
    def Count(cls: Splitter) -> int:
        return len([x for x in cls.all if isinstance(x, Splitter)])

    # Recursively walk from the given node to each possible "end" (`None`) node 
    @functools.cache
    def walk(self: Splitter) -> int:
        return (self.left.walk() if self.left else 1) + \
               (self.right.walk() if self.right else 1)

    # Given the input data, recursively create child splitters
    def _calculate(self: Splitter, input: list[str]) -> None:
        if self.left == None:
            # Search down the left side until we find a splitter, or the end 
            col, row = search_column(input, self.x - 1, self.y) 

            if col != -1 and row != -1:
                self.left = Splitter.Create(input, col, row)

        if self.right == None:
            # Search down the right side until we find a splitter, or the end 
            col, row = search_column(input, self.x + 1, self.y)

            if col != -1 and row != -1:
                self.right = Splitter.Create(input, col, row)

# "Execute" the input data, filling in all of th ebeams 
def execute_input(input: list[str]) -> list[str]:
    executed_input: list[str] = [ ]

    # First, take the input data and calculate the "executed" tree 
    for i, line in enumerate(input):
        line = line.strip('\n')

        # Skip first line, it only contains the start node 
        if i == 0:
            executed_input.append(line)
            continue

        curr_line = ""

        # Check each character in the line 
        for j, char in enumerate(line):
            # Grab the character left, right, and above `char`
            left_char = line[j - 1:j] or None
            right_char = line[j + 1:j + 2] or None
            above_char = executed_input[i - 1][j]

            # Right splitter, and the char above is a beam
            if right_char == CHAR_SPLITTER and executed_input[i - 1][j + 1] == CHAR_BEAM:
                curr_line += CHAR_BEAM
                continue 
            
            # Left splitter, and the char above is a beam
            if left_char == CHAR_SPLITTER and executed_input[i - 1][j - 1] == CHAR_BEAM:
                curr_line += CHAR_BEAM
                continue 

            # Otherwise, check if we should convert this character into a beam
            if char == CHAR_EMPTY and (above_char == CHAR_START or above_char == CHAR_BEAM):
                curr_line += CHAR_BEAM
                continue 

            curr_line += char 

        executed_input.append(curr_line)

    return executed_input

# Find the start character
def find_start_location(input: list[str]) -> Tuple[int, int]:
    for y, line in enumerate(input):
        for x, char in enumerate(line):
            if char != CHAR_START:
                continue 

            return (x, y)
    
    return (-1, -1)

# Search down a column until we find a non-beam character, or reach the end 
def search_column(input: list[str], col: int, start_row: int) -> Tuple[int, int]:
    for row in range(start_row, len(input)):
        char = input[row][col]

        if char == CHAR_BEAM:
            continue 

        return (col, row) 
    
    return (-1, -1)

def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} [input.txt]")
        return 
    
    with open(sys.argv[1]) as f:
        data = f.readlines()

    executed_input = execute_input(data)

    # Find the start point
    (start_x, start_y) = find_start_location(executed_input)

    # Search down until we find the first splitter 
    col, row = search_column(executed_input, start_x, start_y + 1)
    root_splitter = Splitter.Create(executed_input, col, row)

    path_count = root_splitter.walk()

    # Print the "executed" input
    for line in executed_input:
        print(line)

    print("")

    # answers for input.txt (puzzle input)
    # part 1 = 1581
    # part 2 = 73007003089792

    # answers for input2.txt (example input)
    # part 1 = 21
    # part 2 = 40

    print(f"Splitter count (part 1) = {Splitter.Count()}")
    print(f"Path count (part 2) = {path_count}")

if __name__ == '__main__':
    main()
